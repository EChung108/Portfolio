-------------------------------------------------------------------------------
--
-- Title       : ALU
-- Design      : Microprocessor
-- Author      : Ethan Chung - 2160550
-- Company     : University of Birmingham
--
-------------------------------------------------------------------------------
--
-- Description: The Arithmetic Logic Unit (ALU) is what deals with the calculations
--				given to the microprocessor by the instruction stream. It uses the data
--				fetched from the memory and the opcode to decide what data to use and
--				what operation to perform on the given data.
--
-------------------------------------------------------------------------------
--********************************* ALU *************************************--
-- Stating and defining libraries used within the ALU program
library ieee;
use ieee.std_logic_1164.all; 
use ieee.std_logic_signed.all; 


entity alu_test is 
-- Setting up registers used within the ALU program
  port ( a, b: in std_logic_vector(31 downto 0);  
             opcode: in std_logic_vector(5 downto 0);  
             c, c_buffer, c_buffer2: out std_logic_vector(31 downto 0);	   
			 z, n: out std_logic;  
			 valid: out std_logic;
			clock, enable_input: in std_logic); 
end entity alu_test; 

--main body of the code
architecture dataflow of alu_test is 
--set up signal used within the program
	signal c_input: std_logic_vector(31 downto 0); 
begin

	process
	begin
   
--defining what operation to perform on the data inputted into a and b when certain
--opcodes have been put in
  c_input <= a + b when opcode="001010" 	 
  else a - b when opcode="001000" 
  else abs a when opcode="000110" 
  else -a when opcode="001110"
  else abs b when opcode="000010"
  else -b when opcode="001101"
  else a or b when opcode="001111"
  else not a when opcode="001011"
  else not b when opcode="000011"
  else a and b when opcode="000101"
  else a xor b when opcode="000001";
 
--If instructions are invalid then change output, c, to 0
   if valid = '0' then				 
	   c <=	X"00000000";
   else
--If instructions are valid, then allow data to transfer from signal to output register
	   c <= c_input;
	   end if;
	  
	  if c = X"00000000" then	 -- if c is zero, raise z flag
		  z<= '1';
	  else
		  z <= '0';
	  end if;
	  if c <X"00000000" then   -- if c is negative, raise n flag
		  n <= '1';
	  else
		  n <= '0';
	  end if; 
		 
	  	wait until rising_edge(clock); -- tells compiler to only proceed when clock is on rising edge
		
	  end process; 

end architecture dataflow; 

