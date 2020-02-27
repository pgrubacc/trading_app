import React from "react";
import TableCell from "./TableCell";

const TableBody = props => {
  return (
    <tbody>
      {props.data.map(cell => (
        <tr key={cell.string_id}>
          <TableCell  cell={cell} />
        </tr>
      ))}
    </tbody>
  );
};

export default TableBody;
