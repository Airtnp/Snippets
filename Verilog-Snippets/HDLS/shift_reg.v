module shift_reg(Q, Dout, Din, clock);
  parameter size = 8;
  input clock, Din;
  output Dout;
  output [size-1:0] Q;

  reg [size-1:0] Q;

  always @ (posedge clock)
  begin
    Q[size-2:0] <= Q[size-1:1];
    Q[size-1]   <= Din;
  end

  assign Dout = Q[0];
endmodule
