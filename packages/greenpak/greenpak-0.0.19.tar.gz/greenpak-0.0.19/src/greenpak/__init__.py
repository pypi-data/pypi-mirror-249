"""A library to manage and program GreenPAK devices using USB to I2C adapters."""

# Docs
# https://www.renesas.com/us/en/document/mat/system-programming-guide-slg468246?r=1572991
# https://www.renesas.com/us/en/document/mat/slg47004-system-programming-guide?r=1572991

from greenpak.drivers import GreenPakI2cInterface
from enum import Enum
from typing import Optional, List, Tuple, Set
from dataclasses import dataclass
import time
import re

# TODO: Add a more graceful handling of errors.
# TODO: Add a file with the main() of the command line tool to program, etc.

@dataclass(frozen=True)
class _DeviceInfo:
    """Descriptor of a GreenPak device."""

    type: str
    ro_nvm_pages: List[int]
    erase_mask: int

    def assert_valid(self):
        """Assert that the product passes sanity check."""
        assert isinstance(self.type, str)
        assert len(self.type) > 0
        assert issubclass(self.ro_nvm_pages, list)
        assert len(set(self.ro_nvm_pages)) == len(self.ro_nvm_pages), "Duplicate pages"
        for page_index in self.ro_nvm_pages:
            assert isinstance(page_index, int)
            assert 0 <= page_index <= 15
        assert isinstance(self.erase_mask, int)
        assert 0 <= self.erase_mask <= 255
        assert (self.erase_mask & 0b00011111) == 0


_SUPPORTED_DEVICES = dict(
    [
        (d.type, d)
        for d in [
            _DeviceInfo("SLG46824", [15], 0b10000000),
            _DeviceInfo("SLG46826", [15], 0b10000000),
            _DeviceInfo("SLG46827", [15], 0b10000000),
            _DeviceInfo("SLG47004", [8, 15], 0b11000000),
        ]
    ]
)


class _MemorySpace(Enum):
    """The four memory spaces of a GreenPak."""
    REGISTER = 1
    NVM = 2
    EEPROM = 3
    UNUSED = 4

def read_config_file(file_path: str) -> bytearray:
    """Read a GreenPak SPLD config file.

    Reads the config file, converts to configuration bytes, and asserts that there were no errors.
    Config files are text files with the values of the GreenPak configuration bits. These are the
    output files of the Renesas GreenPAK Designer.

    :param file_path: Path to the file to read.
    :type file_path: str

    :returns: The configuration bits as a bytearray of 256 bytes, in the same representation as the GreenPak's NVM memory.
    :rtype: bytearray
    """
    result = bytearray()
    f = open(file_path, "r")
    first_line = True
    bits_read = 0
    byte_value = 0
    for line in f:
        line = line.rstrip()
        if first_line:
            assert re.match(r"index\s+value\s+comment", line)
            first_line = False
            continue
        assert bits_read < 2048
        m = re.match(r"^([0-9]+)\s+([0|1])\s.*", line)
        assert m
        bit_index = int(m.group(1))
        bit_value = int(m.group(2))
        assert bit_index == bits_read
        assert bit_value in (0, 1)
        # Least signiificant bit first
        byte_value = (byte_value >> 1) + (bit_value << 7)
        assert 0 <= byte_value <= 255
        bits_read += 1
        # Handle last bit of a byte
        if (bits_read % 8) == 0:
            result.append(byte_value)
            byte_value = 0
    assert bits_read == 2048
    assert len(result) == 256
    return result


def write_config_file(file_name: str, data: bytearray | bytes) -> None:
    """Write a GreenPak SPLD config file.

    Writes the given configuration bytes, in the same representation as the GreenPak NVM memory,
    as a GreenPak config file. Config files are text files with the values of the GreenPak
    configuration bits. These are th output files of the Renesas GreenPAK Designer.

    :param file_path: Path to the output file.
    :type file_path: str

    :param data: The configuration bytes to write. ``len(data)`` is asserted to be 256.
    :type data: bytearray or bytes
    """
    assert isinstance(data, (bytearray, bytes))
    assert len(data) == 256
    with open(file_name, "w") as f:
        f.write("index\t\tvalue\t\tcomment\n")
        for i in range(len(data) * 8):
            byte_value = data[i // 8]
            # Bit order in file is least significant bit first.
            bit_value = (byte_value >> (i % 8)) & 0x01
            f.write(f"{i}\t\t{bit_value}\t\t//\n")


def hex_dump(data: bytearray | bytes, start_addr: int = 0) -> None:
    """Print bytes in hex format.

    This utility help function is useful to print binary data such
    as GreenPak configuration bytes.

    :param data: The bytes to dump.
    :type data: bytearray or bytes

    :param start_addr: Allows to assign an index other than zero to the first byte.
    :type start_addr: int

    ."""
    assert isinstance(data, (bytearray, bytes)), type(data)
    assert isinstance(start_addr, int)
    assert start_addr >= 0
    end_addr = start_addr + len(data)
    row_addr = (start_addr // 16) * 16
    while row_addr < end_addr:
        items = []
        for i in range(16):
            addr = row_addr + i
            col_space = " " if i % 4 == 0 else ""
            if addr >= end_addr:
                break
            if addr < start_addr:
                items.append(f"{col_space}  ")
            else:
                items.append(f"{col_space}{data[addr - start_addr]:02x}")
        print(f"{row_addr:02x}: {" ".join(items)}", flush=True)
        row_addr += 16


class GreenpakDriver(GreenPakI2cInterface):
    """Creates a GreenPak driver.

    :param i2c_driver: A compatible I2C driver to use to communicate with the GreenPak devices.
    :type i2c_driver: GreenPakI2cDriver

    :param device_type: A string identifying the target GreenPak device, such as ``"SLG46826"``. This
        must be one of the GreenPak devices supported by this class.
    :type device_type: str

    :param device_control_code: The GreenPak device control code. This is an int in the range [0, 15] that
        identifies the device on the I2C bus. The I2C addresses that the device occupies are derived from
        this control code.
    :type device_control_code: int.
    """

    def __init__(
        self, i2c_driver: GreenPakI2cInterface, device_type: str, device_control_code
    ):
        "Constructor."
        assert isinstance(i2c_driver, GreenPakI2cInterface), type(i2c_driver)
        assert device_type in _SUPPORTED_DEVICES
        assert isinstance(device_control_code, int)
        assert 0 <= device_control_code <= 15
        self.__i2c: GreenPakI2cDriver = i2c_driver
        self.set_device_type(device_type)
        self.set_device_control_code(device_control_code)

    def set_device_control_code(self, device_control_code: int) -> None:
        """Sets the control code of the target GreenPAK device.

        :param device_control_code: The GreenPak device control code to use. This is an int in the range [0, 15] that
            identifies the device on the I2C bus. The I2C addresses that the device occupies are derived from
            this control code.
        :type device_control_code: int.
        """
        assert isinstance(device_control_code, int)
        assert 0 <= device_control_code <= 15
        self.__device_control_code = device_control_code

    def get_device_control_code(self) -> int:
        """Returns the currently set device control code."""
        return self.__device_control_code

    def set_device_type(self, device_type: str) -> None:
        """Set target device type.

        :param device_type: A string identifying the target GreenPak device, such as ``"SLG46826"``. This
            must be one of the GreenPak devices supported by this class.
        :type device_type: str
        """
        assert isinstance(device_type, str)
        self.__device_info = _SUPPORTED_DEVICES[device_type]

    def get_device_type(self) -> str:
        """Returns the currently set device type. Note that this does not actually retrive the device
        type from the device but only retrieve the attribute of this driver. As of Jan 2024, Renesas
        did not publish the NVM bits that identified the device type."""
        return self.__device_info.type

    def __i2c_device_addr(
        self, memory_space: _MemorySpace, control_code: int = None
    ) -> int:
        """Constructs the I2C device address for the given memory space."""
        assert memory_space in (
            _MemorySpace.REGISTER,
            _MemorySpace.NVM,
            _MemorySpace.EEPROM,
            _MemorySpace.UNUSED,
        )
        if control_code is None:
            control_code = self.__device_control_code
        assert 0 <= control_code << 15
        memory_space_table = {
            _MemorySpace.REGISTER: 0b000,
            _MemorySpace.NVM: 0b010,
            _MemorySpace.EEPROM: 0b011,
            _MemorySpace.UNUSED: 0b100
        }
        device_i2c_addr = control_code << 3 | memory_space_table[memory_space]
        assert 0 <= device_i2c_addr <= 127
        return device_i2c_addr

    def __read_bytes(
        self, memory_space: _MemorySpace, start_address: int, n: int
    ) -> bytearray:
        """Read a block of bytes from the given memory space."""
        assert memory_space in (
            _MemorySpace.REGISTER,
            _MemorySpace.NVM,
            _MemorySpace.EEPROM,
        )
        assert 0 <= start_address <= 255
        assert 0 < n
        assert start_address + n <= 256

        # Construct the i2c address.
        device_i2c_addr = self.__i2c_device_addr(memory_space)

        # Write the start address to read.
        ok = self.__i2c.write(device_i2c_addr, bytearray([start_address]))
        assert ok
        resp_bytes = self.__i2c.read(device_i2c_addr, n)

        assert resp_bytes is not None
        assert n == len(resp_bytes)
        return resp_bytes

    def read_register_bytes(self, start_address: int, n: int) -> bytearray:
        """Read a memory block from the REGISTER memory space.

        :param start_address: The address of the first byte to read. Should be in the
            range [0, 255].
        :type start_address: int

        :param n: The number of bytes to read. Should be in the range [0, 256] and should
            not exceed the device memory limit.
        :type b: int

        :returns: The bytes read.
        :rtype: bytearray
        """
        return self.__read_bytes(_MemorySpace.REGISTER, start_address, n)

    def read_nvm_bytes(self, start_address: int, n: int) -> bytearray:
        """Read an arbitrary block of bytes from device's NVM memory space.

        :param start_address: The address of the first byte to read. Should be in the
            range [0, 255].
        :type start_address: int

        :param n: The number of bytes to read. Should be in the range [0, 256] and should
            not exceed the device memory limit.
        :type b: int

        :returns: The bytes read.
        :rtype: bytearray
        """
        return self.__read_bytes(_MemorySpace.NVM, start_address, n)

    def read_eeprom_bytes(self, start_address: int, n: int) -> bytearray:
        """Read an arbitrary block of bytes from device's EEPROM memory space.

        :param start_address: The address of the first byte to read. Should be in the
            range [0, 255].
        :type start_address: int

        :param n: The number of bytes to read. Should be in the range [0, 256] and should
            not exceed the device memory limit.
        :type n: int

        :returns: The bytes read.
        :rtype: bytearray
        """
        return self.__read_bytes(_MemorySpace.EEPROM, start_address, n)

    def __is_page_writeable(self, memory_space: _MemorySpace, page_index: int) -> bool:
        """Returns true if the page is writable by the user. """
        assert memory_space in (_MemorySpace.NVM, _MemorySpace.EEPROM), memory_space
        assert isinstance(page_index, int)
        assert 0 <= page_index <= 15
        read_only =  (memory_space ==_MemorySpace.NVM) and  page_index in self.__device_info.ro_nvm_pages
        return not read_only

    def __write_bytes(
        self, memory_space: _MemorySpace, start_address: int, data: bytearray
    ) -> None:
        """An low level method to write a block of bytes to a device memory space.
        For NVM and EEPROM spaces, the block must exactly one page, the
        page must be erased, and user must wait for the operation to complete.
        """
        assert memory_space in (
            _MemorySpace.REGISTER,
            _MemorySpace.NVM,
            _MemorySpace.EEPROM,
        )
        n = len(data)
        assert 0 <= start_address <= 255
        assert 0 < n
        assert start_address + n <= 256

        # For NVM and EEPROM it must be exactly one page.
        if memory_space in (_MemorySpace.NVM, _MemorySpace.EEPROM):
            assert start_address % 16 == 0
            assert n == 16
            assert self.__is_page_writeable(memory_space, start_address // 16)

        # Construct the device i2c address
        device_i2c_addr = self.__i2c_device_addr(memory_space)

        # We write the start address followed by the data bytes
        payload = bytearray()
        payload.append(start_address)
        payload.extend(data)

        # Write the data
        ok = self.__i2c.write(device_i2c_addr, bytearray(payload))
        assert ok

    def __read_page(self, memory_space: _MemorySpace, page_index: int) -> bool:
        """Read a 16 bytes page of a NVM or EEPROM memory spaces."""
        assert memory_space in (_MemorySpace.NVM, _MemorySpace.EEPROM)
        assert 0 <= page_index <= 15
        device_i2c_addr = self.__i2c_device_addr(memory_space)
        data = self.__read_bytes(memory_space, page_index << 4, 16)
        assert len(data) == 16
        return data

    def __erase_page(self, memory_space: _MemorySpace, page_index: int) -> None:
        """Erase a 16 bytes page of NVM or EEPROM spaces to all zeros. Page must be writable"""
        assert memory_space in (_MemorySpace.NVM, _MemorySpace.EEPROM)
        assert self.__is_page_writeable(memory_space, page_index)

        # Erase only if not already erased.
        if self.__is_page_erased(memory_space, page_index):
            print(
                f"Page {memory_space.name}/{page_index:02d} already erased.", flush=True
            )
            return

        # Erase.
        print(f"Erasing page {memory_space.name}/{page_index:02d}.", flush=True)
        # We erase by writing to the register ERSR byte, and waiting.
        space_mask = {_MemorySpace.NVM: 0x00, _MemorySpace.EEPROM: 0x10}[memory_space]
        erase_mask = self.__device_info.erase_mask | space_mask | page_index
        # TODO: Find a cleaner solution for the errata's workaround.
        self.write_register_bytes(0xE3, bytearray([erase_mask]))
        # Allow the operation to complete. Datasheet says 20ms max.
        time.sleep(0.025)

        # Errata woraround. Perform a dummy write to clear the error from the previous write.
        # This is a workaround for the erase issue describe in the errata at:
        # https://www.renesas.com/us/en/document/dve/slg46824-errata?language=en
        device_i2c_addr = self.__i2c_device_addr(_MemorySpace.REGISTER)
        self.__i2c.write(device_i2c_addr, bytearray([0]), silent=True)

        # Verify that the page is all zeros.
        assert self.__is_page_erased(memory_space, page_index)

    def __is_page_erased(self, memory_space: _MemorySpace, page_index: int) -> bool:
        """Returns true if all 16 bytes of given MVM or EEPROM page are zero.
        Page must be writable..
        """
        assert memory_space in (_MemorySpace.NVM, _MemorySpace.EEPROM)
        assert self.__is_page_writeable(memory_space, page_index)

        data = self.__read_page(memory_space, page_index)
        return all(val == 0 for val in data)

    def __program_page(
        self, memory_space: _MemorySpace, page_index: int, page_data: bytearray
    ) -> None:
        """Program a NVM or EEPROM 16 bytes page. Page must be writeable."""
        assert memory_space in (_MemorySpace.NVM, _MemorySpace.EEPROM)
        assert self.__is_page_writeable(memory_space, page_index)
        assert len(page_data) == 16

        # Do nothing if the page already has the desired value.
        old_data = self.__read_page(memory_space, page_index)
        if old_data == page_data:
            print(f"Page {memory_space.name}/{page_index:02d} no change.", flush=True)
            return

        # Erase the page to all zeros.
        self.__erase_page(memory_space, page_index)

        # Write the new page data.
        print(f"Writing page {memory_space.name}/{page_index:02d}.", flush=True)
        self.__write_bytes(memory_space, page_index << 4, page_data)
        # Allow the operation to complete. Datasheet says 20ms max.
        time.sleep(0.025)

        # Read and verify the page's content.
        actual_page_data = self.__read_page(memory_space, page_index)
        assert actual_page_data == page_data

    def __program_pages(
        self, memory_space: _MemorySpace, start_page_index: int, pages_data: bytearray
    ) -> None:
        """Program one or mage 16 bytes pages of the NVM or EEPROM spaces."""
        assert memory_space in (_MemorySpace.NVM, _MemorySpace.EEPROM)
        assert 0 <= start_page_index <= 15
        assert 1 < len(pages_data)
        assert (len(pages_data) % 16) == 0
        assert (start_page_index << 4) + len(pages_data) <= 256

        num_pages = len(pages_data) // 16
        assert 0 < num_pages
        assert start_page_index + num_pages <= 16
        for i in range(0, num_pages):
            if not self.__is_page_writeable(memory_space, i):
                print(
                    f"Page {memory_space.name}/{i} a read only page, skipping.",
                    flush=True,
                )
            else:
                page_data = pages_data[i << 4 : (i + 1) << 4]
                self.__program_page(memory_space, start_page_index + i, page_data)

    def write_register_bytes(self, start_address: int, data: bytearray) -> None:
        """Write a block of bytes to device's REGISTER memory space.

        The method writes the bytes to the device and asserts that the operation was
        successful.
        
        :param start_address: The address of the first byte to write. Should be in the
            range [0, 255].
        :type start_address: int

        :param data: The bytes to write. ``len(data)`` should be in the range [0, 256] and should
            not exceed the device memory limit.
        :type data: int

        :returns: None.
        """
        self.__write_bytes(_MemorySpace.REGISTER, start_address, data)

    def program_nvm_pages(self, start_page_index: int, pages_data: bytearray) -> None:
        """Program one or more 16 bytes pages of the NVM memory space.
        
        The NVM memory space is made of 16 bytes blocks call pages which are erased and 
        updated as a whole. This methods programs one or more conescutive pages in the NVM
        memory space of the device and asserts that the operation is successful. 
        
        :param start_page_index: The index of the first page that should be programmed with
            ``data``. Should be in the range p0, 15]. For example program from byte at address
            32, use the page index 2.
        :type start_page_index: int

        :param pages_data: The bytes to write. ``len(data)`` should be a multiple of 16.
        :type data: int

        :returns: None.
        """   
        self.__program_pages(_MemorySpace.NVM, start_page_index, pages_data)

    def program_eeprom_pages(self, start_page_index: int, pages_data: bytearray) -> None:
        """Program one or more 16 bytes pages of the EEPROM memory space.
        
        The EEPROM memory space is made of 16 bytes blocks call pages which are erased and 
        updated as a whole. This methods programs one or more conescutive pages in the NVM
        memory space of the device and asserts that the operation is successful. 
        
        :param start_page_index: The index of the first page that should be programmed with
            ``data``. Should be in the range p0, 15]. For example program from byte at address
            32, use the page index 2.
        :type start_page_index: int

        :param pages_data: The bytes to write. ``len(data)`` should be a multiple of 16.
        :type data: int

        :returns: None.
        """         
        self.__program_pages(_MemorySpace.EEPROM, start_page_index, pages_data)

    def reset_device(self) -> None:
        """Reset the device.
        
        Sends a reset command to the device. A reset applies the NVM configuration by copying
        it to the REGISTER spates and brings the device to initial state. Use it after programming
        the NVM to apply the new configuration. The method asserts that the operation was successful

        :returns: None.
        """
        # Set register bit 1601 to reset the device.
        self.write_register_bytes(0xC8, bytearray([0x02]))
        # Allow the operation to complete.
        # TODO: Check with the datasheet what time period to use here.
        time.sleep(0.1)

    def scan_greenpak_device(self, control_code: int) -> bool:
        """Test if a GreenPak device exists.
        
        GreenPak devices are identified by their 4 bits 'cotrol code' which derive the 
        I2C addresses that they occupy on the I2C bus. This method tests if a GreenPak
        device of a given code exists on the I2C bus. To qualify, all the 4 I2C address
        that are derived from this control code need to respond to I2C operations. 

        :param control_code: The control code of the GreenPak device to test. Should 
           be in the range [0, 15].
        :type control_code: int

        :returns: True if the device was found, False otherwise.
        :rtype: bool
        """
        assert 0 <= control_code <= 15
        ok = True
        # All three memory spaces need to be present.
        for memory_space in (_MemorySpace.REGISTER, _MemorySpace.NVM, _MemorySpace.EEPROM, _MemorySpace.UNUSED):   
            device_i2c_addr = self.__i2c_device_addr(_MemorySpace.REGISTER, control_code)
            ok = ok and self.__i2c.write(device_i2c_addr, bytearray([]), silent=True)
        return ok

    def scan_greenpak_devices(self) -> None:
        """Scans the I2C bus for GreenPak devices.
        
        Scans each of the possible device control codes and returns list of control codes
        of devices that were found on the I2C bus.

        :returns: A sorted list with the control codes for which ``scan_greenpak_device`` returned True.
        :rtype: List[int]
        """
        result = []
        for control_code in range(16):
            if self.scan_greenpak_device(control_code):
                result.append(control_code)
        return result
