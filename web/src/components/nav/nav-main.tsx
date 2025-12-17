"use client";
import { type Icon } from "@tabler/icons-react";
import { NavLink, useLocation } from "react-router-dom";

import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import type { LucideIcon } from 'lucide-react';

export function NavMain({
  items,
}: {
  items: {
    title: string;
    url: string;
    icon?: Icon | LucideIcon;
    label: string;
  }[];
}) {
  const { pathname } = useLocation();

  return (
    <SidebarGroup>
      <SidebarGroupContent className="flex flex-col gap-2">
        <SidebarMenu>
          {items.map((item) => {
            const isActive = pathname === item.url || pathname.startsWith(item.url + "/");
            return (
              <>
                <SidebarGroupLabel>{item.label}</SidebarGroupLabel>
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton tooltip={item.title} asChild isActive={isActive}>
                    <NavLink to={item.url}>
                      {item.icon && <item.icon />}
                      <span>{item.title}</span>
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              </>
            );
          })}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  );
}
