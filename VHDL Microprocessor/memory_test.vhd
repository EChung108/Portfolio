-------------------------------------------------------------------------------
--
-- Title       : Memory
-- Design      : Microprocessor
-- Author      : Ethan Chung - 2160550
-- Course      : Electronic Engineering
--
-------------------------------------------------------------------------------
--
-- Description : The memory is the storage for the microprocessor and holds the 
--				 data and instructions. The memory locations wanted come in from 
--  			 the instruction stream and the memory will output the data
--				 inside the memory location specified. It can also overwrite the
--				 data stored in a specified memory location from the output of the 
--				 microprocessor
--
-------------------------------------------------------------------------------	  
--*************************** Memory (RAM) **********************************--
-- Stating and defining libraries used within the Memory program
library ieee;
use ieee.std_logic_1164.all; 
use ieee.std_logic_unsigned.all; 

-- Setting up registers used within the Memory program
entity memory_test is
	port ( addr1, addr2, addr3: in std_logic_vector(4 downto 0);  
	addr3_buff1, addr3_buff2, addr3_buff3: out std_logic_vector(4 downto 0);
	d_in: in std_logic_vector(31 downto 0); 					  
	check: out std_logic_vector(31 downto 0); 					  
	d_out1, d_out2: out std_logic_vector(31 downto 0);	         
	valid: in std_logic;
	clock, enable_input: in std_logic);
end entity memory_test;

--start of main body of code
architecture dataflow of memory_test is                             	 
type rom_array is array (0 to 31) of std_logic_vector(31 downto 0); -- Defining ROM memory as 32 locations each of 32-bit length
signal rom_mem: rom_array := ( 										   
		X"00000000", X"00000000", X"00018011", X"00016E5A",         -- Initiallisng data inside each memory location
		X"000036B7", X"000126ED", X"00016D79", X"0000014C", 
		X"00014E6B", X"00008EA6", X"000132FA", X"0000B97C", 
		X"0000FD2A", X"00003DC0", X"000065EB", X"0000455A", 
		X"00013D89", X"000125ED", X"0000DB20", X"00017A12", 
		X"0000404A", X"0000B0C8", X"0000015B", X"0000F4A4", 
		X"0000FBCC", X"0000D281", X"0000B806", X"00002E5B", 
		X"0000BCE3", X"00007C82", X"00012EE9", X"00000000"); 	
-- Setting up signals used in th memory program		
signal addr1_valid, addr2_valid: std_logic_vector(4 downto 0); 
signal 	d_inbuff: std_logic_vector(31 downto 0);
begin
   process
   begin  
-- if instructions are valid, then move the values from certain registers to signals	   
   if valid = '1' then
	
	   
	   addr3_buff1 <= addr3;

	   d_inbuff <= d_in;
	   addr1_valid <= addr1; 
	   addr2_valid <= addr2;
	
-- if instructions are not valid, then change singal values to 0
	else 
	addr3_buff1 <= "00000";	
	d_inbuff <=X"00000000";

	end if;
-- put data from given memory loaction into registers d_out1 and d_out2
		d_out1 <= rom_mem(conv_integer(addr1_valid));   	
	d_out2 <= rom_mem(conv_integer(addr2_valid));  
	
-- Move write back address along pipeline 	
	addr3_buff2 <= addr3_buff1;
	
-- write back the value of d_in into given memory location	
	rom_mem(conv_integer(addr3_buff1)) <= d_in;
	
-- put value from given memory address into register check
check <= rom_mem(conv_integer(addr3_buff2));   

-- tells program to only proceed when clock is on rising edge
	wait until rising_edge(clock); 

   end process;  

end architecture dataflow;
	
	
 

