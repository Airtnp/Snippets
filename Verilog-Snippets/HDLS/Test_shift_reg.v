module Test_shift_reg;

  parameter half_period = 50;
  parameter size = 8;
  
  wire [size-1:0] Q;
  wire Dout;
  reg  clock, Din;
  
  shift_reg UUT (Q, Dout, Din, clock);
  
  initial begin
    #0    clock = 0; Din = 0;
	 #500  Din = 1;
	 #1000  Din = 0; 
  end
  
  always #half_period clock = ~clock;

  initial #2000 $stop;

endmodule
