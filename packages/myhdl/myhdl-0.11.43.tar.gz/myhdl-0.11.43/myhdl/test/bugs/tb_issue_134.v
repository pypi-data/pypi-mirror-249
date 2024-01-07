module tb_issue_134;

reg ab_in_a;
reg ab_in_b;
wire ab_out_a;
wire ab_out_b;

initial begin
    $from_myhdl(
        ab_in_a,
        ab_in_b
    );
    $to_myhdl(
        ab_out_a,
        ab_out_b
    );
end

issue_134 dut(
    ab_in_a,
    ab_in_b,
    ab_out_a,
    ab_out_b
);

endmodule
