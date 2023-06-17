-------------------------------------------------------------------------------
--
-- Title       : Instruction stream
-- Design      : Microprocessor
-- Author      : Ethan Chung - 2160550
-- Course      : Electronic Engineering
--
-------------------------------------------------------------------------------
--
-- Description : The instruction stream acts as the inputs to the microprocessor 
--				 from an external source. In this assignment, the instruction set
-- 				 was given as r2+r3+r4+r5+r6-r7-r8-r9-r10-r11+r12+r13+r14+r15+r16
--				 -r17-r18-r19-20-r21+r22+r23+r24+r25+r26-r27-r28-r29-r30
--
-------------------------------------------------------------------------------
--*********************** Instruction Stream ********************************--
-- Stating and defining libraries used within the instruction stream program
 library ieee;
use ieee.std_logic_1164.all; 
use ieee.std_logic_unsigned.all; 
 


entity instruction_stream is  
-- setting up reigsters used in the Instruction stream program
	port (instruct: out std_logic_vector(31 downto 0); 
	clk: in std_logic;
	enable: in std_logic;
	valid: in std_logic); 
	
end instruction_stream;


-- Start of main body of code
architecture dataflow of instruction_stream is
begin

   	  process is
	   begin  


 	   --wait until the next rising edge of the clock and for enable to be 1 to proceed
	   wait until rising_edge(clk) and enable = '1';
	   instruct <= B"001010_00010_00011_00001_00000000000"; -- r2+r3 goes into r1	
	   
	   
	   wait until rising_edge(clk) and enable = '1';  -- no-op 
	   wait until rising_edge(clk) and enable = '1';  -- no-op

	   
	   wait until rising_edge(clk) and enable = '1';
	   instruct <= B"001010_00111_01000_11111_00000000000";-- r7+r8 goes into	r31
	   
	   
	   wait until rising_edge(clk) and enable = '1'; 
	   wait until rising_edge(clk) and enable = '1';

	   
	   	   wait until rising_edge(clk) and enable = '1';
	   instruct <= B"001010_00100_00001_00001_00000000000"; --r4+r1 goes into r1  
	   
	   
	   wait until rising_edge(clk) and enable = '1';
	   wait until rising_edge(clk) and enable = '1';


	   	   wait until rising_edge(clk) and enable = '1';
	   instruct <= B"001010_01001_11111_11111_00000000000"; --r9+r31 goes into r31 
	   
	   
	   wait until rising_edge(clk) and enable = '1'; 
	   wait until rising_edge(clk) and enable = '1';

	  	   
	   wait until rising_edge(clk) and enable = '1';
	   instruct <= B"001010_00101_00001_00001_00000000000"; --r5+r1 goes into r1  
	   
	   
	   wait until rising_edge(clk) and enable = '1';
	   wait until rising_edge(clk) and enable = '1';
 
	   
	   	  wait until rising_edge(clk) and enable = '1';
	  instruct <= B"001010_01010_11111_11111_00000000000";  --r10+r31 goes into r31	 
	  
	  
	  wait until rising_edge(clk) and enable = '1'; 
	  wait until rising_edge(clk) and enable = '1';

	   
	    wait until rising_edge(clk) and enable = '1';
	   instruct <= B"001010_00110_00001_00001_00000000000";  --r6+r1 goes into r1  
	   
	   
	   wait until rising_edge(clk) and enable = '1'; 
	   wait until rising_edge(clk) and enable = '1';
	

	  wait until rising_edge(clk) and enable = '1';
	  instruct <= B"001010_01011_11111_11111_00000000000"; --r11+r31 goes into r31 
	  
	  
	  wait until rising_edge(clk) and enable = '1';
	  wait until rising_edge(clk) and enable = '1';
	  
	  
	  wait until rising_edge(clk) and enable = '1';
	  instruct <= B"001010_01100_00001_00001_00000000000";	--r12+r1 goes into r1  
	  
	  
	  wait until rising_edge(clk) and enable = '1';
	  wait until rising_edge(clk) and enable = '1';  


	   	 wait until rising_edge(clk) and enable = '1';
	 instruct <= B"001010_10001_11111_11111_00000000000"; --r17+r31 goes into r31  
	 
	 
	 wait until rising_edge(clk) and enable = '1'; 
	 wait until rising_edge(clk) and enable = '1'; 


	  
	 wait until rising_edge(clk) and enable = '1';
	 instruct <= B"001010_01101_00001_00001_00000000000";	--r13+r1 goes into r1  
	 
	 
	 wait until rising_edge(clk) and enable = '1';
	 wait until rising_edge(clk) and enable = '1';   


	    wait until rising_edge(clk) and enable = '1'; 
	 instruct <= B"001010_10010_11111_11111_00000000000"; --r18+r31 goes into r31 
	 
	 
	 wait until rising_edge(clk) and enable = '1';  
	 wait until rising_edge(clk) and enable = '1';
	   
	 
	 wait until rising_edge(clk) and enable = '1';
	 instruct <= B"001010_01110_00001_00001_00000000000";	--r14+r1 goes into r1 
	 
	 
	   wait until rising_edge(clk) and enable = '1';
	   wait until rising_edge(clk) and enable = '1';
	   
	   
		 wait until rising_edge(clk) and enable = '1';
	 instruct <= B"001010_10011_11111_11111_00000000000"; --r19+r31 goes into r31 
	 
	 
	 wait until rising_edge(clk) and enable = '1';
	 wait until rising_edge(clk) and enable = '1';  

	  
  	 wait until rising_edge(clk) and enable = '1';
	 instruct <= B"001010_01111_00001_00001_00000000000";	--r15+r1 goes into r1 
	 
	 
	 wait until rising_edge(clk) and enable = '1';
	 wait until rising_edge(clk) and enable = '1';  

	   
	   	wait until rising_edge(clk) and enable = '1';
	instruct <= B"001010_10100_11111_11111_00000000000"; --r20+r31 goes into r31	
	
	
	wait until rising_edge(clk) and enable = '1';  
	wait until rising_edge(clk) and enable = '1';   


	 wait until rising_edge(clk) and enable = '1';
	 instruct <= B"001010_10000_00001_00001_00000000000";	--r16+r1 goes into r1
	 
	 
	 wait until rising_edge(clk) and enable = '1';
	 wait until rising_edge(clk) and enable = '1';  
	 

	wait until rising_edge(clk) and enable = '1';
	instruct <= B"001010_10101_11111_11111_00000000000"; --r21+r31 goes into r31  
	
	
	wait until rising_edge(clk) and enable = '1'; 
	wait until rising_edge(clk) and enable = '1';  

	
	 wait until rising_edge(clk) and enable = '1';
	 instruct <= B"001010_10110_00001_00001_00000000000"; --r22+r1 goes into r1	  
	 
	 
	 wait until rising_edge(clk) and enable = '1';  
	 wait until rising_edge(clk) and enable = '1';  


	 wait until rising_edge(clk) and enable = '1';  
	instruct <= B"001010_11011_11111_11111_00000000000"; --r27+r31 goes into r31  
	
	
	wait until rising_edge(clk) and enable = '1'; 
	wait until rising_edge(clk) and enable = '1';
	
	 
	wait until rising_edge(clk) and enable = '1';
	instruct <= B"001010_10111_00001_00001_00000000000"; -- r23+r1 goes into r1	 
	
	
	wait until rising_edge(clk) and enable = '1';
	wait until rising_edge(clk) and enable = '1';


	 	wait until rising_edge(clk) and enable = '1';
	instruct <= B"001010_11100_11111_11111_00000000000";  --  r28+r31 goes into r31	 
	
	
	wait until rising_edge(clk) and enable = '1'; 
	wait until rising_edge(clk) and enable = '1';  


	wait until rising_edge(clk) and enable = '1';
	instruct <= B"001010_11000_00001_00001_00000000000"; --r24+r1 goes into r1
	
	
	wait until rising_edge(clk) and enable = '1'; 
	wait until rising_edge(clk) and enable = '1'; 


	  	wait until rising_edge(clk) and enable = '1'; 
	instruct <= B"001010_11101_11111_11111_00000000000"; --r29+r31 goes into r31  
	
	
	wait until rising_edge(clk) and enable = '1';
	wait until rising_edge(clk) and enable = '1';  


	wait until rising_edge(clk) and enable = '1';
	instruct <= B"001010_11001_00001_00001_00000000000";  --r25+r1 goes into r1  
	
	
	wait until rising_edge(clk) and enable = '1';
	wait until rising_edge(clk) and enable = '1'; 


	  	wait until rising_edge(clk) and enable = '1';
	instruct <= B"001010_11110_11111_11111_00000000000"; --r30+r31 goes into r31 
	
	
	wait until rising_edge(clk) and enable = '1';  
	wait until rising_edge(clk) and enable = '1';   

	   	   		
	wait until rising_edge(clk) and enable = '1';
	instruct <= B"001010_11010_00001_00001_00000000000"; --r26+r1 goes into r1
	
	
	wait until rising_edge(clk) and enable = '1';
	wait until rising_edge(clk) and enable = '1'; 
	wait until rising_edge(clk) and enable = '1'; 
	

	
	wait until rising_edge(clk) and enable = '1';
	instruct <= B"001000_00001_11111_11111_00000000000";	--r1-r31 goes into r31 	
	
	wait until rising_edge(clk) and enable = '1'; 
	wait until rising_edge(clk) and enable = '1'; 
	
	   
	   wait until rising_edge(clk) and enable = '1';
	instruct <= B"100001_00001_11111_11111_00000000000"; --invalid opcode to hold final answer
	   wait;
	   end process;
end architecture;
