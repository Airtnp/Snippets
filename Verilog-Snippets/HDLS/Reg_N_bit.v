module Reg_N_bits (Q, Din, clock, load);
  parameter size = 8;
  input clock, load;
  input [size-1:0] Din;
  output [size-1:0] Q;

  reg [size-1:0] Q;

  always @ (posedge clock)
  begin
    if (load) Q <= Din; 
  end
endmodule
