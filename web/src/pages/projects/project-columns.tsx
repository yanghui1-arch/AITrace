import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
} from "@/components/ui/dropdown-menu";
import { type ColumnDef } from "@tanstack/react-table";
import {
  MoreHorizontal,
  ArrowUp,
  ArrowDown,
  Trash2,
  Pencil,
  List,
  Clock,
  DollarSign,
} from "lucide-react";

export type Project = {
  name: string;
  description: string;
  cost: number;
  avgDuration: number;
  lastUpdateTimestamp: string;
};

export const projectColumns: ColumnDef<Project>[] = [
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate")
        }
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
  },
  {
    accessorKey: "name",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          className="w-full justify-center"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          <span className="inline-flex items-center justify-center gap-1">
            <span className="w-4 inline-flex justify-end">
              <List className="h-4 w-4" />
            </span>
            <span className="font-semibold">Name</span>
            <span className="w-4 inline-flex justify-start">
              {column.getIsSorted() === "asc" ? (
                <ArrowDown className="h-4 w-4" />
              ) : (
                <ArrowUp className="h-4 w-4" />
              )}
            </span>
          </span>
        </Button>
      );
    },
  },
  {
    accessorKey: "avgDuration",
    header: () => (
      <div className="w-full flex justify-center">
        <span className="inline-flex items-center gap-1">
          <Clock className="h-4 w-4" />
          <span className="font-semibold">Duration (avg.)</span>
        </span>
      </div>
    ),
    cell: ({ row }) => {
      const avgDuration = row.original.avgDuration;
      return <div className="font-medium">{avgDuration + "s"}</div>;
    },
  },
  {
    accessorKey: "cost",
    header: () => (
      <div className="w-full flex justify-center">
        <span className="inline-flex items-center gap-1">
          <DollarSign className="h-4 w-4" />
          <span className="font-semibold">Cost</span>
        </span>
      </div>
    ),
    cell: ({ row }) => {
      const cost = parseFloat(row.getValue("cost"));
      const formatted = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      }).format(cost);
      return <div className="font-medium">{formatted}</div>;
    },
  },
  {
    accessorKey: "lastUpdateTimestamp",
    header: () => (
      <div className="w-full flex justify-center">
        <span className="font-semibold">Last Update</span>
      </div>
    ),
    cell: ({ row }) => {
      const lastUpdateTimestamp = row.getValue("lastUpdateTimestamp") as string;
      return (
        <div className="text-center font-medium">{lastUpdateTimestamp}</div>
      );
    },
  },
  {
    id: "action",
    cell: ({ row }) => {
      const project = row.original;
      console.log(project);

      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-40" align="end">
            <DropdownMenuGroup>
              <DropdownMenuItem>
                Edit
                <DropdownMenuShortcut>
                  <Pencil className="h-4 w-4" />
                </DropdownMenuShortcut>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <span className="text-red-400">Delete</span>
                <DropdownMenuShortcut>
                  <Trash2 className="h-4 w-4" />
                </DropdownMenuShortcut>
              </DropdownMenuItem>
            </DropdownMenuGroup>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    },
  },
];
