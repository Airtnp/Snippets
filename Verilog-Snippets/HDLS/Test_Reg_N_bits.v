module Test_Reg_N_bits;

  parameter half_period = 50;
  parameter size = 8;
  
  wire [size-1:0] Q;
  reg  clock, load;
  reg  [size-1:0] Din;
  
  Reg_N_bits UUT (Q, Din, clock, load);
  
  initial begin
    #0    clock = 0; Din = 0; load = 0;
	 #500  Din = 8'hff;
	 #300  load = 1;
	 #200  load = 0; 
	 #100  Din = 8'hf0;
	 #300  load = 1; 
  end
  
  always #half_period clock = ~clock;

  initial #2000 $stop;

endmodule
