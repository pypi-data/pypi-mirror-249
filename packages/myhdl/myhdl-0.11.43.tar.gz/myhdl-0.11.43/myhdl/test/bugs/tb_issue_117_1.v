module tb_issue_117_1;

reg clk;
reg sdi;
wire [7:0] pdo;
reg [1:0] sel;

initial begin
    $from_myhdl(
        clk,
        sdi,
        sel
    );
    $to_myhdl(
        pdo
    );
end

issue_117_1 dut(
    clk,
    sdi,
    pdo,
    sel
);

endmodule
