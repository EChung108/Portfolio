-------------------------------------------------------------------------------
--
-- Title       : Microprocessor (test bench)
-- Design      : Microprocessor
-- Author      : Ethan Chung - 2160550 
-- Course      : Electronic Engineering
-------------------------------------------------------------------------------
--
-- Description : The Microprocessor is the total itegration of each part that has 
--				 been designed. It is tasked with dealing with operations that are
--               given to it from the instruction stream and output the required 
--				 solutions and write them back into the given memory location
--
-------------------------------------------------------------------------------	
--************** Microprocessor *******************
-- setting up the libraries used
library ieee; 
use ieee.std_logic_1164.all; 
use ieee.std_logic_signed.all; 
use ieee.numeric_std.all;

entity compalu is
end entity compalu;

architecture test of compalu is	
--setting up signals used within the Microprocessor program
signal instruct_trans: std_logic_vector(31 downto 0); 
signal opcode_in: std_logic_vector(5 downto 0) :="000000";											  
signal in1, in2, in3: std_logic_vector(4 downto 0);
signal alu_in1, alu_in2, alu_out, alu_trans, output: std_logic_vector(31 downto 0) :=X"00000000";	  
signal sigz, sign: std_logic := '0'; 																  
signal clk: std_logic;  
signal enable: std_logic;
signal valid_check: std_logic;
begin

   process is 		--constantly changing clk value when code is running
   begin 			-- Period per full clock cycle = 10 ns
    clk <= '0';
	wait for 5 ns;
    clk <= '1';
    wait for 5 ns;
   end process;
   
g1: entity work.instruction_stream(dataflow) -- run architecture named dataflow in program instruction_stream
	port map( instruct => instruct_trans, clk => clk,  -- transfer named registers into named signals
	enable => enable, valid => valid_check);
      
   g2: entity work.decoder_test(divide)	-- run architecture named divide in program named decoder_test
	   port map ( instruct_input => instruct_trans, instruct1 => in1, instruct2 => in2, 
	   instruct3buff2 => in3, opcode => opcode_in, clock => clk, valid_trans => valid_check, 
	   enable_trans => enable, output_check => output);

	  g3: entity work.memory_test(dataflow) -- run architecture named dataflow in program named memory_test
		  port map ( addr1 => in1, addr2 => in2, d_out1 => alu_in1, d_out2 => alu_in2, 
		  addr3 => in3, d_in => alu_trans, check => output, valid => valid_check,
		  clock => clk, enable_input => enable);  	 
	

	  g4: entity work.alu_test(dataflow) -- run architecture named dataflow in program named alu_test 	
		  port map ( a => alu_in1, b => alu_in2, opcode => opcode_in, c => alu_out,
		  z => sigz, n => sign, clock => clk, enable_input => enable); 
   		 
alu_trans <= alu_out;	-- transfer value of alu_out to alu_trans to be written back to memory
			 
end architecture test;  



	
	   
	
	   	   







