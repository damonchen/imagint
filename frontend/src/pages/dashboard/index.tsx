import { useEffect, useMemo, useState } from 'react'
import { CopyIcon } from '@radix-ui/react-icons'
import { IconChevronDown } from '@tabler/icons-react'
import { Button } from '@/components/custom/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Search } from '@/components/search'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import ThemeSwitch from '@/components/theme-switch'
import { TopNav } from '@/components/top-nav'
import { UserNav } from '@/components/user-nav'
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu'
import { Layout, LayoutBody, LayoutHeader } from '@/components/custom/layout'
import { RecentSales } from './components/recent-sales'
import { Overview } from './components/overview'
import { useSelf } from '@/provider/self-account-provider';
import { Textarea } from '@/components/ui/textarea'
import { useCurrentChatStore } from '@/store'
import { createChatMessage, createChat } from '@/api/chat'


interface PromptParams {

}

export default function Dashboard() {
  const { account } = useSelf();
  const { chat, setChat, setMessage } = useCurrentChatStore();
  const [prompt, setPrompt] = useState('');
  const [params, setParams] = useState<PromptParams|null>(null);

  const onMessageGenerate = async () => {
    // 调用后台的api生成图片，然后图片以框架的方式显示
    if(!chat.id) {
      const newChat = await createChat(prompt)
      setChat({...newChat, messages: [] });
    }

    const chatId = chat.id;
    const message = await createChatMessage(chatId, prompt, params);
    setMessage(message);

    // 新增一个message
    const messages = [...chat.messages, message];
    setChat({ ...chat, messages });
  }

  return (
    <Layout>
      {/* ===== Top Heading ===== */}
      {/* <LayoutHeader>
        <TopNav links={topNav} />
        <div className='ml-auto flex items-center space-x-4'>
          <Search />
          <ThemeSwitch />
          <UserNav />
        </div>
      </LayoutHeader> */}

      {/* ===== Main ===== */}
      <LayoutBody className='space-y-4'>
        <div className="flex gap-4">
          {/* Left side - Prompt input and settings */}
          <div className="w-1/3 space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Image Generation</CardTitle>
                <CardDescription>Enter your prompt to generate AI images</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2 relative">
                  {/* <Label htmlFor="prompt">Prompt</Label> */}
                  <Textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    id="prompt"
                    placeholder="What do you want to see?"
                    className="h-40"
                  />
                  <div className='absolute bottom-2 left-2'>
                    <div className="flex flex-wrap gap-2">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button
                            variant="outline"
                            size="sm"
                            className="flex items-center gap-1"
                          >
                            <span>Aspect Ratio</span>
                            <IconChevronDown className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent>
                          <DropdownMenuItem>
                            Square (1:1)
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            Portrait (2:3)
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            Landscape (3:2)
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            Wide (16:9)
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>


                      {/* <Button
                        variant="outline"
                        size="sm"
                        className="flex items-center gap-1"
                      >
                        <input type="checkbox" className="h-3 w-3" />
                        <span>Square Aspect</span>
                      </Button> */}

                      <Button
                        variant="outline"
                        size="sm"
                        className="flex items-center gap-1"
                      >
                        {/* <input type="checkbox" className="h-3 w-3" /> */}
                        <span>No Style</span>
                      </Button>

                      <Button
                        variant="outline"
                        size="sm"
                        className="flex items-center gap-1"
                      >
                        {/* <input type="checkbox" className="h-3 w-3" /> */}
                        <span>No Color</span>
                      </Button>

                      <Button
                        variant="outline"
                        size="sm"
                        className="flex items-center gap-1"
                      >
                        {/* <input type="checkbox" className="h-3 w-3" /> */}
                        <span>No Lighting</span>
                      </Button>

                      <Button
                        variant="outline"
                        size="sm"
                        className="flex items-center gap-1"
                      >
                        {/* <input type="checkbox" className="h-3 w-3" /> */}
                        <span>No Composition</span>
                      </Button>
                    </div>

                  </div>
                </div>


                <div className="flex justify-between">
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      className="flex items-center gap-1"
                    >
                      <input type="checkbox" className="h-3 w-3" />
                      <span>Negative Prompt</span>
                    </Button>

                    <Button
                      variant="outline"
                      size="sm"
                      className="flex items-center gap-1"
                    >
                      <input type="checkbox" className="h-3 w-3" />
                      <span>High Quality</span>
                    </Button>
                  </div>
  

                </div>

                <div className='flex items-center space-x-2'>
                    <Button variant="outline">Clear</Button>
                    <Button variant="outline">Random</Button>
                    <Button variant="default" onClick={onMessageGenerate}>Generate</Button>
                  </div>
              </CardContent>
            </Card>
          </div>

          {/* Right side - Results display */}
          <div className="w-2/3">
            <div className="flex flex-col space-y-8">
              {/* Message container */}
              {chat?.messages?.map((message, index) => (
                <div key={index} className="flex flex-col space-y-4">
                  {/* Prompt text */}
                  <div className="text-right text-sm text-gray-600">
                    {message.prompt}
                  </div>

                  {/* Image grid */}
                  <div className="grid grid-cols-3 gap-4">
                    {message.images?.map((image, imageIndex) => (
                      <div key={imageIndex} className="relative group">
                        {/* Thumbnail image */}
                        {!image.thumbnailUrl ? (
                          <div className="w-full h-48 bg-gray-100 rounded-lg flex items-center justify-center">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 dark:border-gray-100"></div>
                          </div>
                        ) : (
                          <img
                            src={image.thumbnailUrl}
                            alt={`Generated image ${imageIndex + 1}`}
                            className="w-full h-48 object-cover rounded-lg"
                          />
                        )}

                        {/* Download button */}
                        <button
                          className="absolute top-2 right-2 p-2 bg-black/50 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                          onClick={() => {
                            // Download original image
                            const link = document.createElement('a')
                            link.href = image.originalUrl
                            link.download = `generated-image-${index}-${imageIndex}.png`
                            link.click()
                          }}
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="white"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          >
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                            <polyline points="7 10 12 15 17 10" />
                            <line x1="12" y1="15" x2="12" y2="3" />
                          </svg>
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>


        {/* <div className='flex items-center justify-between space-y-2'>
          <h1 className='text-2xl font-bold tracking-tight md:text-3xl'>
            Dashboard
          </h1>
          <div className='flex items-center space-x-2'>
            <Button>Download</Button>
          </div>
        </div>
        <Tabs
          orientation='vertical'
          defaultValue='overview'
          className='space-y-4'
        >
          <div className='w-full pb-2'>
            <TabsList>
              <TabsTrigger value='overview'>Overview</TabsTrigger>
              <TabsTrigger value='analytics'>Analytics</TabsTrigger>
              <TabsTrigger value='reports'>Reports</TabsTrigger>
              <TabsTrigger value='notifications'>Notifications</TabsTrigger>
            </TabsList>
          </div>
          <TabsContent value='overview' className='space-y-4'>
            <div className='grid gap-4 sm:grid-cols-2 lg:grid-cols-4'>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium'>
                    Total Revenue
                  </CardTitle>
                  <svg
                    xmlns='http://www.w3.org/2000/svg'
                    viewBox='0 0 24 24'
                    fill='none'
                    stroke='currentColor'
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth='2'
                    className='h-4 w-4 text-muted-foreground'
                  >
                    <path d='M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6' />
                  </svg>
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>$45,231.89</div>
                  <p className='text-xs text-muted-foreground'>
                    +20.1% from last month
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium'>
                    Subscriptions
                  </CardTitle>
                  <svg
                    xmlns='http://www.w3.org/2000/svg'
                    viewBox='0 0 24 24'
                    fill='none'
                    stroke='currentColor'
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth='2'
                    className='h-4 w-4 text-muted-foreground'
                  >
                    <path d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2' />
                    <circle cx='9' cy='7' r='4' />
                    <path d='M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75' />
                  </svg>
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>+2350</div>
                  <p className='text-xs text-muted-foreground'>
                    +180.1% from last month
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium'>Sales</CardTitle>
                  <svg
                    xmlns='http://www.w3.org/2000/svg'
                    viewBox='0 0 24 24'
                    fill='none'
                    stroke='currentColor'
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth='2'
                    className='h-4 w-4 text-muted-foreground'
                  >
                    <rect width='20' height='14' x='2' y='5' rx='2' />
                    <path d='M2 10h20' />
                  </svg>
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>+12,234</div>
                  <p className='text-xs text-muted-foreground'>
                    +19% from last month
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium'>
                    Active Now
                  </CardTitle>
                  <svg
                    xmlns='http://www.w3.org/2000/svg'
                    viewBox='0 0 24 24'
                    fill='none'
                    stroke='currentColor'
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth='2'
                    className='h-4 w-4 text-muted-foreground'
                  >
                    <path d='M22 12h-4l-3 9L9 3l-3 9H2' />
                  </svg>
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>+573</div>
                  <p className='text-xs text-muted-foreground'>
                    +201 since last hour
                  </p>
                </CardContent>
              </Card>
            </div>
            <div className='grid grid-cols-1 gap-4 lg:grid-cols-7'>
              <Card className='col-span-1 lg:col-span-4'>
                <CardHeader>
                  <CardTitle>Overview</CardTitle>
                </CardHeader>
                <CardContent className='pl-2'>
                  <Overview />
                </CardContent>
              </Card>
              <Card className='col-span-1 lg:col-span-3'>
                <CardHeader>
                  <CardTitle>Recent Sales</CardTitle>
                  <CardDescription>
                    You made 265 sales this month.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <RecentSales />
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs> */}
      </LayoutBody>
    </Layout>
  )
}

const topNav = [
  {
    title: 'Overview',
    href: 'dashboard/overview',
    isActive: true,
  },
  {
    title: 'Customers',
    href: 'dashboard/customers',
    isActive: false,
  },
  {
    title: 'Products',
    href: 'dashboard/products',
    isActive: false,
  },
  {
    title: 'Settings',
    href: 'dashboard/settings',
    isActive: false,
  },
]
