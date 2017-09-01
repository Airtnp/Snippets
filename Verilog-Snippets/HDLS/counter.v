module counter_N_bit (clock, clear, CE, Q);
  parameter N = 3;
  input 	clock, clear, CE;
  output	[N-1:0] 	Q;
  reg		[N-1:0] 	Q;

  always @  (posedge clock) 
    if (clear == 1'b1) Q <= 0; 
    else if (CE == 1'b1) Q <= Q + 1;
endmodule 
