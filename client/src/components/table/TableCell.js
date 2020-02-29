import React from "react";

const TableCell = (props) => {
    return (
        Object.keys(props.cell).map((cellData, i) => {
            if (cellData === "string_id") {
                return null
            }
            return <td key={i}>{props.cell[cellData]}</td>
        })
    );
};

export default TableCell;
