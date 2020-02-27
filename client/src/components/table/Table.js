import React from "react";
import TableHeader from "./TableHeader";
import TableBody from "./TableBody";
const Table = props => {
  return (
    <table>
      <TableHeader />
      <TableBody data={props.data} />
    </table>
  );
};
export default Table;
