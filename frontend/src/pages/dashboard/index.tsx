import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { IconChevronDown } from '@tabler/icons-react'
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu'
import { Layout, LayoutBody } from '@/components/custom/layout'
import { Textarea } from '@/components/ui/textarea'
import { useCurrentChatStore } from '@/store'
import { createChat, createChatMessage } from '@/api/chat'
import { Button } from "@/components/ui/button"
import { useState } from "react"

const Message = (message, onMessageEdit, onMessageGenerate) => {

    return <div className="flex flex-col p-2">
        <div className="text-sm text-gray-600">
            {/* 6月6日 */}
        </div>
        <div className="text-sm text-gray-600">
            <div>
                {message.prompt}
            </div>
            {/* 生成一张AI自然语言算法流程图,包括最大似然估计、角注法和隐马尔可夫链等等平均概率算法流程。它汇聚成上万个变量，概率大数定律概率最大。每个节点都有概率参数，代码模块可"智能化交叉变异"，中间结果大写。 */}
        </div>
        <div className="grid grid-cols-4 gap-2">
            {message.images?.map((image) => (
                <div key={image.id} className="relative aspect-square">
                    <img
                        src={image.thumbnailUrl}
                        alt={`Flow diagram ${image.id}`}
                        className="w-full h-full object-cover"
                    />
                    <div className="absolute top-2 right-2 w-full h-full flex items-center justify-center">
                        <Button
                            variant="ghost"
                            className="text-white hover:text-white bg-black/50"
                            onClick={() => window.open(image.url, '_blank')}
                        >
                            <IconChevronDown className="w-4 h-4" />
                        </Button>
                    </div>
                </div>
            ))}
        </div>
        <div className="flex items-center gap-4 text-sm text-gray-600">
            <button className="flex items-center gap-1" onClick={onMessageEdit}>
                <span>重新编辑</span>
            </button>
            <button className="flex items-center gap-1" onClick={onMessageGenerate}>
                <span>再次生成</span>
            </button>
        </div>
    </div>
}


export default function Dashboard() {
    const { chat, setChat, setMessage } = useCurrentChatStore();
    const [prompt, setPrompt] = useState('');
    // 用于存储生成图片的参数
    // const [image, setImage] = useState(null);

    const [params, setParams] = useState({
        'type': 'text2image',
        'model': 'qwen-image',        // 模型类型， 如stable-diffusion, qwen-image, flux.dev
        'size': '1:1',
    });

    const onMessageGenerate = async () => {
        // 调用后台的api生成图片，然后图片以框架的方式显示
        let chatId = chat.id;
        if (!chatId) {
            const newChat = await createChat(prompt)
            setChat({ ...newChat, messages: [] });
            chatId = newChat.id
        }

        const message = await createChatMessage(chatId, prompt, params);
        message.prompt = prompt
        message.params = params;

        setMessage(message);

        // 新增一个message
        const messages = [...chat.messages, message];
        setChat({ ...chat, messages });
    }

    const onMessageEdit = (message) => {
        setPrompt(message.prompt);
    }

    const onMessageReGenerate = async (message) => {
        const chatId = chat.id;
        const params = message.params;
        const prompt = message.prompt;

        setParams(params);

        const newMessage = await createChatMessage(chatId, prompt, params);
        newMessage.prompt = prompt
        newMessage.params = params;
        setMessage(newMessage);

        // 新增一个message
        const messages = [...chat.messages, newMessage];
        setChat({ ...chat, messages });
    }

    return <Layout>
        <LayoutBody>
            {
                chat.messages?.map((message) => (
                    <Message key={message.id} message={message} onMessageEdit={onMessageEdit} onMessageGenerate={onMessageReGenerate} />
                ))
            }

            <div className="flex flex-col gap-4 border rounded-xl bg-gray-100">
                <div className="flex items-center p-2">
                    <div className="flex items-center space-x-2">

                    </div>
                    <Textarea
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        id="prompt"
                        placeholder="What do you want to see?"
                        className="h-40"
                    />
                </div>

                <div className="flex items-center justify-between w-full p-2">
                    <div className="flex items-center gap-2">
                        <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                                <Button variant="outline" className="gap-2">
                                    <span>Image</span>
                                    <IconChevronDown size={16} />
                                </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent>
                                <DropdownMenuItem>
                                    Image Generation
                                </DropdownMenuItem>
                                <DropdownMenuItem>
                                    Video Generation
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>

                        <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                                <Button variant="outline" className="gap-2 ml-2">
                                    <span>1:1</span>
                                    <IconChevronDown size={16} />
                                </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent>
                                <DropdownMenuItem>
                                    1:1
                                </DropdownMenuItem>
                                <DropdownMenuItem>
                                    16:9
                                </DropdownMenuItem>
                                <DropdownMenuItem>
                                    4:3
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                    </div>
                    <div className="flex items-center gap-2">
                        <Button onClick={onMessageGenerate}>Generate</Button>
                    </div>

                </div>

            </div>
        </LayoutBody>
    </Layout>
}