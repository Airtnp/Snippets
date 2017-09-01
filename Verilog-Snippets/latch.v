module SRLatch(s, r, q, qbar);
    input s, r;
    output q, qbar;

    // q = s + (~r) & q;
    // S R Q Q+
    // 0 0 0 0
    // 0 0 1 1 hold
    //
    // 0 1 0 0 
    // 0 1 1 0 reset
    //
    // 1 0 0 1 
    // 1 0 1 1 set
    //
    // 1 1 0 X
    // 1 1 1 X not allowed

    nor(q, r, qbar);
    nor(qbar, s, q);

endmodule

module GatedSRLatch(G, S, R, Q, Qbar);
    input G, S, R;
    output Q, Qbar;

    // G S R Q Q+
    // 0 - - Q Q  locked
    // 1 0 0 Q Q  hold
    // 1 0 1 Q 0  reset
    // 1 1 0 Q 1  set
    // 1 1 1 Q X  not allowed

    wire S1, R1;
    and(S1, S, G);
    and(R1, R, G);
    nor(Qbar, S1, Q);
    nor(Q, S1, Qbar);

endmodule


module DLatch(G, D, Q, Qbar);
    input G, D;
    output reg Q, Qbar;

    always @ (D or G) begin
        if (G) begin
            Q <= D;
            Qbar <= ~D;
        end
        else
            Q <= Q;
            Qbar <= Qbar;
    end
endmodule