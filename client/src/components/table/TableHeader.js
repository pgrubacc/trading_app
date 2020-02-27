import React from "react";

const TableHeader = () => {
  return (
    <thead  className="table-head">
      <tr>
        <th>Sell CCY</th>
        <th>Sell Amount</th>
        <th>Buy CCY</th>
        <th>Buy Amount</th>
        <th>Rate</th>
        <th>Date booked</th>
      </tr>
    </thead>
  );
};

export default TableHeader;
