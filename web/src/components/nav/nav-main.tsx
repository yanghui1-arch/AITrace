"use client";

import { type Icon } from "@tabler/icons-react";
import { useState } from "react";

import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

export function NavMain({
  items,
}: {
  items: {
    title: string;
    url: string;
    icon?: Icon;
    label: string;
  }[];
}) {
  const [activeItem, setActiveItem] = useState<string>("Overview");

  return (
    <SidebarGroup>
      <SidebarGroupContent className="flex flex-col gap-2">
        <SidebarMenu>
          {items.map((item) => (
            <>
              <SidebarGroupLabel>{item.label}</SidebarGroupLabel>
              <SidebarMenuItem key={item.title}>
                <SidebarMenuButton tooltip={item.title} 
                  onClick={() => setActiveItem(item.title)}
                  isActive={activeItem === item.title}>
                  {item.icon && <item.icon />}
                  <span>{item.title}</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </>
          ))}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  );
}
