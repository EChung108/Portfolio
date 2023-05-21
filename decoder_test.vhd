-------------------------------------------------------------------------------
--
-- Title       : Decoder
-- Design      : Microprocessor
-- Author      : Ethan Chung - 2160550   
--Course	   : Electronic Engineering	
--
-------------------------------------------------------------------------------
--
-- Description : The decoder is tasked with seperating the instructions from the 
--				 insctruction stream into the correct parts, such as opcode or
--               memory data location 1,2 and 3.      
-------------------------------------------------------------------------------	
--************************* Decoder *****************************************--
-- Stating and defining libraries used within the Decoder program
library ieee; 
use ieee.std_logic_1164.all; 
use ieee.std_logic_signed.all; 
 

-- setting up registers used with the decoder program
entity decoder_test is	 
	port ( opcode, opcode_buff1, opcode_buff2: out std_logic_vector(5 downto 0); -- 6 bit register
	instruct1, instruct2, instruct3: out std_logic_vector(4 downto 0); -- 5 bit register
	instruct3buff, instruct3buff2 : out std_logic_vector(4 downto 0);
	instruct_input: in std_logic_vector(31 downto 0); -- 32 bit register 
	instruct_valid, instruct_buff, instruct_buff2: out std_logic_vector(31 downto 0);
	valid_trans, enable_trans: out std_logic; -- 1 bit register
	clock: in std_logic;
	output_check: in std_logic_vector(31 downto 0));
end decoder_test;


--beginning of main body of code
architecture divide of decoder_test is  
-- initialising signals used in code
signal enable: std_logic; 
signal valid: std_logic;

begin
	   
	   process is
	   begin   
		   
		-- move the instruction stream along pipeline   
		   instruct_buff<=instruct_input;	
		   
		--input insctruction is broken down into opcode 
		--and instructions 1, 2 and 3
		opcode_buff1 <= instruct_input(31 downto 26);

		opcode <= opcode_buff1;
	
 		instruct1 <= instruct_input(25 downto 21);	   
 
		instruct2 <= instruct_input(20 downto 16);	   

		instruct3 <= instruct_input(15 downto 11); 
		
 
 -- buffer instruction 3 as would arrive at ALU to early
instruct3buff <= instruct3;
instruct3buff2 <= instruct3buff;

-- checks for valid write back location and opcode
-- if write back location = 0 or opcode is invalid, change signal valid to 0	
		if instruct3 = "00000" then
			valid <= '0';

		elsif opcode >= "010000" then 
			valid <= '0';

		elsif opcode = "000100" then
			valid <= '0';

		elsif opcode = "000111" then
			valid <= '0';

		elsif opcode = "001001" then
			valid <= '0';

		elsif opcode = "001100" then
			valid <= '0';  
-- if everything ok, enable and valid signals go to 1			
   else 	
	   enable <= '1';
	valid <= '1';

	end if;
-- transfer signals to regsiters
			enable_trans <= enable;
			valid_trans <= valid; 
					
			wait until rising_edge(clock); -- tells program to only proceed when clock is on rising edge
			
			
	end process;	

end architecture;
