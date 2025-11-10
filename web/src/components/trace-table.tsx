import type { Trace } from "@/pages/projects/track/trace-columns";
import { DataTable } from "./data-table";
import { RowPanelContent } from "./data-table/data-table-row-panel";
import type { ColumnDef } from "@tanstack/react-table";

interface TraceTableProps<TValue> {
  columns: ColumnDef<Trace, TValue>[];
  data: Trace[];

}

export function TraceTable<TValue>({
  columns,
  data,
}: TraceTableProps<TValue>) {
    return (
      <div className="container mx-auto py-2">
        <DataTable data={data} columns={columns}>
          <RowPanelContent<Trace>>
            {(rowData) => (<></>)}
          </RowPanelContent>
        </DataTable>
      </div>
    );
  }