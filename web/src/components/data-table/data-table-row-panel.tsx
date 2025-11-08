import React from "react";

interface RowPanelContentProps<TData> {
  children: (rowData: TData) => React.ReactNode;
}

/**
 * Replacement component and render logic is in DataTable component.
 * only pass render function while calling it.
 */
export function RowPanelContent<TData>({ children }: RowPanelContentProps<TData>) {
  return null;
}
