`include "flip-flop.v"


module Mux2x1(i0, i1, select, out);
    input i0, i1, select;
    output reg out;
    
    always @ (i0, i1, select) begin
        case (select):
            1'b0: out <= i0;
            1'b1: out <= i1;
            default: out <= 0;
        endcase
    end
endmodule


module Mux4x4(CX0, CX1, CX2, CX3, AN0, AN1, AN2, AN3, O);
	parameter N = 7;
	input [N - 1:0] CX0, CX1, CX2, CX3;
	input AN0, AN1, AN2, AN3;
	output reg [N - 1:0] O;
	
	always @ * begin
		if (AN0 == 1'b1) O = CX0;
		else if (AN1 == 1'b1) O = CX1;
		else if (AN2 == 1'b1) O = CX2;
		else if (AN3 == 1'b1) O = CX3;
		else O = 0;
	end
	
endmodule

module Register(data_in, clk, reset, data_out);
    parameter N = 4;
    input [N-1:0] data_in;
    input clk, reset;
    output reg [N-1:0] data_out;

    always @ (posedge reset or posedge clk) begin
        if (reset == 1'b1)
            data_out <= N'b0;
        else
            data_out <= data_in;
    end

    // Or
    /*
        DFF dff0(clk, rst, data_in[0], data_out[0]);
        DFF dff1(clk, rst, data_in[1], data_out[1]);
	    DFF dff2(clk, rst, data_in[2], data_out[2]);
	    DFF dff3(clk, rst, data_in[3], data_out[3]);
    */

endmodule


module TriBuffer(A, B, C);
	parameter N = 7;
	input [N - 1:0] A;
	input B;
	output [N - 1:0] C;
	assign C = (B == 1'b1) ? A : 7'bZ;
endmodule

module TriBufferN(out, in, ce);
    parameter N = 3;
    input [N - 1:0] in;
    output tri [N - 1:0] out;
    input [N - 1:0] ce;
    genvar i;
    generate
        for (i = 0; i < N; i = i + 1) begin : generate_block_tribuffer // to satisfy ISE
            bufif1 (out[i], in[i], ce); // buff[i] for non-ISE
        end
    endgenerate
endmodule