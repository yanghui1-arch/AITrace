import React from "react";

interface RowPanelContentProps<TData> {
  children: (rowData: TData) => React.ReactNode;
}

/**
 * Replacement component and render logic is in DataTable component.
 * only pass render function while calling it.
 */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export function RowPanelContent<TData>(_unused: RowPanelContentProps<TData>) {
  return null;
}
