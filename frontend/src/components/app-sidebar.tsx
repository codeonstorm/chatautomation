"use client"

import * as React from "react"
import {
  AudioWaveform,
  BookOpen,
  Bot,
  Command,
  Frame,
  GalleryVerticalEnd,
  Map,
  PieChart,
  Settings2,
  SquareTerminal,

  Globe,
  PlusCircle,
  MoreHorizontal,
  MessageCircle
} from "lucide-react"

import { NavMain } from "@/components/nav-main"
import { NavProjects } from "@/components/nav-projects"
import { NavUser } from "@/components/nav-user"
import { TeamSwitcher } from "@/components/team-switcher"
import { AddDomainDialog } from "@/components/forms/add-domain-dialog"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,

  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import { Button } from "@/components/ui/button"
import { useAppDispatch } from "@/redux/store/hooks"
import { Domain } from "@/types/domain"
import { useSelector } from 'react-redux';
import { RootState } from "@/redux/store/store";

import { useRouter } from "next/navigation";
import { useAuth } from "@/context/auth-context";
import { getDomains } from "@/services/domain";
import { addDomains } from "@/redux/store/features/domain/domain";
import { useEffect, useState } from "react";

// This is sample data.
const data = {
  // user: {
  //   name: "Ankit",
  //   email: "a@example.com",
  //   avatar: "/avatars/shadcn.jpg",
  // },
  teams: [
    {
      name: "AI Chatbot Builder",
      logo: GalleryVerticalEnd,
      plan: "Standard",
    },
    {
      name: "Acme Corp.",
      logo: AudioWaveform,
      plan: "Startup",
    },
    {
      name: "Evil Corp.",
      logo: Command,
      plan: "Free",
    },
  ],
  navMain: [
    {
      title: "Models",
      url: "#",
      icon: Bot,
      items: [
        {
          title: "Genesis",
          url: "#",
        },
        {
          title: "Explorer",
          url: "#",
        },
        {
          title: "Quantum",
          url: "#",
        },
      ],
    },
    {
      title: "Settings",
      url: "#",
      icon: Settings2,
      items: [
        {
          title: "General",
          url: "#",
        },
        {
          title: "Team",
          url: "#",
        },
        {
          title: "Billing",
          url: "#",
        },
        {
          title: "Limits",
          url: "#",
        },
      ],
    },
    {
      title: "Documentation",
      url: "#",
      icon: BookOpen,
      items: [
        {
          title: "Introduction",
          url: "#",
        },
        {
          title: "Get Started",
          url: "#",
        },
        {
          title: "Tutorials",
          url: "#",
        },
        {
          title: "Changelog",
          url: "#",
        },
      ],
    },
  ],
  projects: [
    {
      name: "Training Progress",
      url: "/dashboard/chatbots/training",
      icon: Frame,
    },
    {
      name: "Sales & Marketing",
      url: "#",
      icon: PieChart,
    },
  ]
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const domains:Domain[] = useSelector((state: RootState) => state.domains);

  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const dispatch = useAppDispatch();

    useEffect(() => {
      if (!isLoading) {
        if (!isAuthenticated) {
          router.push("/login");
        }

        if (!user) {
          router.push("/login");
        }
  
        const domains = async () => {
          if (!user) {
            router.push("/login");
            return
          }
          const domains: Domain[] = await getDomains(user.services[0].id);
          dispatch(addDomains(domains));
        };
  
        domains();
      }
    }, [isAuthenticated, isLoading, router]);


  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={data.teams} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
        <NavProjects projects={data.projects} />
        <SidebarGroup>
          <SidebarGroupLabel>Domains</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <AddDomainDialog/>
            </SidebarMenuItem>
            {domains.slice(0, 4).map((domain) => (
              <SidebarMenuItem key={domain.uuid}>
                <SidebarMenuButton className={domain.status === "enabled" ? "text-custom-gold" : ""}>
                  <Globe className="h-4 w-4 mr-2" />
                  <span>{domain.domain}</span>
                  <span
                    className={`ml-auto text-xs ${domain.status === "enabled" ? "text-green-500" : "text-yellow-500"}`}
                  >
                    {domain.status}
                  </span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
            {
            domains.length > 2 && 
            <SidebarMenuItem>
            <SidebarMenuButton className="text-sidebar-foreground/70">
              <MoreHorizontal className="text-sidebar-foreground/70" />
              <span>More</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
            }

          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <NavUser/>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
