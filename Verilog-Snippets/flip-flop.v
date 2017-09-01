module DFlipFlop(clk, D, Q);
    input clk, D;
    output reg Q;

    always @ (posedge clk) begin
        Q <= D;
    end
endmodule


module DFlipFlopN(clk, D, Q);
    parameter N = 4;
	input clk;
	input [N - 1:0] D;
    output reg [N - 1:0] Q;

    always @ (posedge clk) begin
        Q <= D;
    end
endmodule

module DFlipFlopWithSynchReset(clk, D, reset, Q);
    input D, clk, reset;
    output reg Q;
    always @ (posedge clk) begin
        if (reset) begin
            Q <= 1'b0;
        end else
            Q <= D;
        end
    end
endmodule

module DFlipFlopWithASynchReset(clk, D, reset, Q);
    input D, clk, reset;
    output reg Q;
    always @ (posedge clk or posedge reset) begin
        if (reset) begin
            Q <= 1'b0;
        end else
            Q <= D;
        end
    end
endmodule 

module JKFlipFlop(clk, J, K, Q);
    input clk, J, K;
    output reg Q;
    // Q+ = JQ' + K'Q
    always @ (posedge clk) begin
        case({J, K})
            2'b00: Q <= Q;
            2'b01: Q <= 1'b0;
            2'b10: Q <= 1'b1;
            default: Q <= ~Q;
        endcase
    end
endmodule

module TFlipFlop(clk, reset, T, Q);
    input clk, reset, T;
    output reg Q;

    // Q+ = T'Q+TQ' = T \oplus Q
    always @ (posedge clk) begin
        if (reset)
            Q <= 1'b0;
        else if (T)
            Q <= Q;
        else
            Q <= ~Q;
    end
endmodule

module FlopPCA(preset, reset, Q, Qbar, clk, data);
    input preset, reset, clk, data;
    output Q, Qbar;
    reg Q;

    assign Qbar = ~Q;

    always @ (negedge clk)
        Q = data;
    
    always @ (reset or preset) begin 
        if (reset) assign Q = 0;
        else if (preset) assign Q = 1;
        else deassign Q;
    end
endmodule