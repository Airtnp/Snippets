module Test_Top;

  parameter half_period = 50;
  parameter size = 8;
  
  wire [size-1:0] RxReg_out;
  reg  clock, reset, valid, Data_in;
  
  Top UUT (clock, reset, valid, Data_in, RxReg_out);
  
  initial begin
    #0    clock = 0; valid = 0; Data_in = 0; reset = 1;
	 #100  reset = 0;
	 #240  valid = 1; Data_in = 1;
    #100  valid = 0;	
    #700  Data_in = 0;	 
//	 #400    valid = 1; Data_in = 1;
	 #0    valid = 1; Data_in = 1;
    #100  valid = 0;	Data_in = 0; 
	 #100  Data_in = 1;
	 #100  Data_in = 0;
	 #100  Data_in = 1;
	 #100  Data_in = 0;    	 
	 #100  Data_in = 1;
	 #100  Data_in = 0;
  end
  
  always #half_period clock = ~clock;

//  initial #2000 $stop;
  initial #3000 $stop;
endmodule
