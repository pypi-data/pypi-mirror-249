module tb_issue_98_1;

wire sda;
wire scl;
wire sda_i;
reg sda_o;
wire scl_i;
reg scl_o;

initial begin
    $from_myhdl(
        sda_o,
        scl_o
    );
    $to_myhdl(
        sda,
        scl,
        sda_i,
        scl_i
    );
end

issue_98_1 dut(
    sda,
    scl,
    sda_i,
    sda_o,
    scl_i,
    scl_o
);

endmodule
