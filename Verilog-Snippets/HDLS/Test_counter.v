module Test_counter;
  parameter half_period = 50;
  parameter counter_size = 3;
  
  wire [counter_size-1:0] Q;
  reg  clock, reset, CE;
  
  counter_N_bit UUT (clock, reset, CE, Q);
  
  initial begin
    #0    clock = 0; reset = 1; CE = 0;
	 #100  reset = 0;
	 #160  CE = 1; 
	 #600  CE = 0;
  end
  
  always #half_period clock = ~clock;

  initial #2000 $stop;
endmodule