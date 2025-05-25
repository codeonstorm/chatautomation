'use client'

import { useParams } from 'next/navigation'
import { useMemo } from 'react'
import {
  TagIcon,
  BotIcon,
  CodeIcon,
  BoxesIcon,
  EyeIcon,
  SettingsIcon,
  HistoryIcon,
  TestTubeIcon,
  BugIcon,
  WebhookIcon,
  PieChart,
  Folder,
  type LucideIcon,
} from 'lucide-react'

import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from '@/components/ui/sidebar'

type Project = {
  name: string
  url: string
  icon: LucideIcon
}

export function NavProjects({
  baseProjects = [],
}: {
  baseProjects?: Project[]
}) {
  const { isMobile } = useSidebar()
  const params = useParams()

  const projects = useMemo(() => {
    if (typeof params.id === 'string') {
      return [
        {
          name: 'Chatbot',
          url: `/dashboard/chatbots/${params.id}`,
          icon: BotIcon,
        },
        {
          name: 'Intents',
          url: `/dashboard/chatbots/${params.id}/intents`,
          icon: SettingsIcon,
        },
        {
          name: 'Entities',
          url: `/dashboard/chatbots/${params.id}/entities`,
          icon: BoxesIcon,
        },
        {
          name: 'Webhook',
          url: `/dashboard/chatbots/${params.id}/webhook`,
          icon: WebhookIcon,
        },
        {
          name: 'Preview',
          url: `/dashboard/chatbots/${params.id}/preview`,
          icon: EyeIcon,
        },
        {
          name: 'Embedding',
          url: `/dashboard/chatbots/${params.id}/train`,
          icon: BugIcon,
        },
        {
          name: 'Test',
          url: `/dashboard/chatbots/${params.id}/testing`,
          icon: TestTubeIcon,
        },
        {
          name: 'Histories',
          url: `/dashboard/chatbots/${params.id}/history`,
          icon: HistoryIcon,
        },
        {
          name: 'Sentiment Analysis',
          url: `/dashboard/chatbots/${params.id}/sentiment`,
          icon: TagIcon,
        },
        {
          name: 'Embed Code',
          url: `/dashboard/chatbots/${params.id}/embedcode`,
          icon: CodeIcon,
        },
        ...baseProjects,
      ]
    }
    return baseProjects
  }, [params.id, baseProjects])

  return (
    <SidebarGroup className="group-data-[collapsible=icon]:hidden">
      <SidebarGroupLabel>Tools</SidebarGroupLabel>
      <SidebarMenu>
        {projects.map((item) => (
          <SidebarMenuItem key={item.name}>
            <SidebarMenuButton asChild>
              <a href={item.url}>
                <item.icon />
                <span>{item.name}</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        ))}
      </SidebarMenu>
    </SidebarGroup>
  )
}
