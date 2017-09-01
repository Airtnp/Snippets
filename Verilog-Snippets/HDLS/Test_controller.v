module Test_controller;
  parameter half_period = 50;
  
  wire RxReg_ld, count_en, count_clr;
  reg  clock, reset, valid, comp_out;
  
  controller UUT (clock, reset, valid, comp_out, count_en, count_clr, RxReg_ld);
  
  initial begin
    #0    clock = 0; valid = 0; comp_out = 1; reset = 1;
	 #100  reset = 0;
	 #190  valid = 1; 
	 #100  valid = 0;
	 #600  comp_out = 0; 
  end
  
  always #half_period clock = ~clock;

  initial #2000 $stop;
endmodule

