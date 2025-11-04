import { type Table } from "@tanstack/react-table";
import { X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DataTableViewOptions } from "@/components/data-table/data-table-view-options";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog";
import { Label } from "../ui/label";

interface DataTableToolbarProps<TData> {
  table: Table<TData>;
  hasCreateProjectComponent: boolean;
}

export function DataTableToolbar<TData>({
  table,
  hasCreateProjectComponent = false,
}: DataTableToolbarProps<TData>) {
  const isFiltered = table.getState().columnFilters.length > 0;

  return (
    <div className="flex items-center justify-between">
      <div className="flex flex-1 items-center space-x-2">
        <Input
          placeholder="Filter projects..."
          value={(table.getColumn("name")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("name")?.setFilterValue(event.target.value)
          }
          className="h-8 w-[150px] lg:w-[250px]"
        />
        {isFiltered && (
          <Button
            variant="ghost"
            onClick={() => table.resetColumnFilters()}
            className="h-8 px-2 lg:px-3"
          >
            Reset
            <X />
          </Button>
        )}
      </div>
      <div className="flex items-center gap-2">
        <DataTableViewOptions table={table} />
        {hasCreateProjectComponent && <Dialog>
          <DialogTrigger asChild>
            <Button size="sm">Create Project</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Create Project</DialogTitle>
              <DialogDescription>
                Create a new project for AITrace
              </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4">
              <div className="grid gap-3">
                <Label>Project Name</Label>
                <Input id="name-1" name="name" placeholder="New project name" />
              </div>
              <div className="grid gap-3">
                <Label>Description</Label>
                <Input
                  id="username-1"
                  name="username"
                  placeholder="Brief description"
                />
              </div>
            </div>
            <DialogFooter className="justify-between">
              <DialogClose asChild>
                <Button type="button" variant="destructive">
                  Cancel
                </Button>
              </DialogClose>
              <DialogClose asChild>
                <Button type="button" variant="secondary">
                  Create
                </Button>
              </DialogClose>
            </DialogFooter>
          </DialogContent>
        </Dialog>}
      </div>
    </div>
  );
}
