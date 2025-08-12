import { useEffect, useMemo, useCallback } from "react"
import { IconChevronDown, IconX, IconChevronUp, IconChevronDown as IconChevronDownIcon } from '@tabler/icons-react'
import { useQueryClient, useQuery } from '@tanstack/react-query'
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu'
import { Layout, LayoutBody } from '@/components/custom/layout'
import { Textarea } from '@/components/ui/textarea'
import { useCurrentChatStore } from '@/store'
import type { Image, Message } from '@/store/chat'
import { createChat, createChatMessage, getChatMessage, getChatMessages, getCurrentChat } from '@/api/chat'
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { getStorage, setStorage, removeStorage } from '@/storage'

// Image Viewer Modal Component
const ImageViewer = ({
    images,
    currentIndex,
    isOpen,
    onClose,
    onNavigate
}: {
    images: Image[],
    currentIndex: number,
    isOpen: boolean,
    onClose: () => void,
    onNavigate: (direction: 'prev' | 'next') => void
}) => {
    if (!isOpen) return null;

    const currentImage = images[currentIndex];
    const hasPrev = currentIndex > 0;
    const hasNext = currentIndex < images.length - 1;

    return (
        <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center">
            <div className="relative w-full h-full flex items-center justify-center">
                {/* Close button - top right */}
                <Button
                    variant="ghost"
                    size="icon"
                    className="absolute top-4 right-4 z-10 bg-white/20 hover:bg-white/30 text-white"
                    onClick={onClose}
                >
                    <IconX className="w-6 h-6" />
                </Button>

                {/* Navigation buttons - right side middle */}
                <div className="absolute right-4 top-1/2 transform -translate-y-1/2 flex flex-col gap-4 z-10">
                    <Button
                        variant="ghost"
                        size="icon"
                        className={`bg-white/20 hover:bg-white/30 text-white ${!hasPrev ? 'opacity-50 cursor-not-allowed' : ''}`}
                        onClick={() => hasPrev && onNavigate('prev')}
                        disabled={!hasPrev}
                    >
                        <IconChevronUp className="w-6 h-6" />
                    </Button>
                    <Button
                        variant="ghost"
                        size="icon"
                        className={`bg-white/20 hover:bg-white/30 text-white ${!hasNext ? 'opacity-50 cursor-not-allowed' : ''}`}
                        onClick={() => hasNext && onNavigate('next')}
                        disabled={!hasNext}
                    >
                        <IconChevronDownIcon className="w-6 h-6" />
                    </Button>
                </div>

                {/* Main image */}
                <img
                    src={currentImage.imageUrl}
                    alt={`Image ${currentIndex + 1}`}
                    className="max-w-full max-h-full object-contain"
                />

                {/* Image counter */}
                <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black/50 text-white px-3 py-1 rounded-full text-sm">
                    {currentIndex + 1} / {images.length}
                </div>
            </div>
        </div>
    );
};

const ChatMessage = ({ message, onMessageEdit, onMessageGenerate }: { message: Message, onMessageEdit: (message: Message) => void, onMessageGenerate: (message: Message) => void }) => {

    const placeholderImages = useMemo(() => Array(message.count).fill(0), [message.count]);
    const [imageViewerOpen, setImageViewerOpen] = useState(false);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);

    const openImageViewer = (index: number) => {
        setCurrentImageIndex(index);
        setImageViewerOpen(true);
    };

    const closeImageViewer = () => {
        setImageViewerOpen(false);
    };

    const navigateImage = (direction: 'prev' | 'next') => {
        if (direction === 'prev' && currentImageIndex > 0) {
            setCurrentImageIndex(currentImageIndex - 1);
        } else if (direction === 'next' && currentImageIndex < (message.images?.length || 0) - 1) {
            setCurrentImageIndex(currentImageIndex + 1);
        }
    };

    return <div className="flex flex-col p-2">
        <div className="text-sm text-gray-600">
            {/* 6月6日 */}
        </div>
        <div className="text-sm text-gray-600">
            <div>
                {message.prompt}
            </div>
        </div>
        <div className="grid grid-cols-4 gap-2 p-2">
            {
                message.status === 'running' && (
                    <div className="w-full h-full flex items-center">
                        {
                            placeholderImages.map((value) => {
                                return <div key={value} className="w-10 h-10 border-t-transparent border-b-transparent border-r-transparent border-l-transparent border-t-gray-600 border-r-gray-600 border-l-gray-600 border-b-gray-600 rounded-full animate-spin"></div>
                            })
                        }
                    </div>
                )
            }
            {message.images ? message.images.map((image: Image, index: number) => (
                <div key={image.id} className="relative aspect-square">
                    <img
                        src={image.thumbnailUrl}
                        alt={`Flow diagram ${image.id}`}
                        className="w-full h-full object-cover cursor-pointer hover:opacity-80 transition-opacity"
                        onClick={() => openImageViewer(index)}
                    />
                    <div className="absolute top-2 right-2 ">
                        <Button
                            variant="link"
                            className="text-white hover:text-white bg-black/50"
                            onClick={() => window.open(image.imageUrl, '_blank')}
                        >
                            <IconChevronDown className="w-4 h-4" />
                        </Button>
                    </div>
                </div>
            )) : placeholderImages.map((_, index) => {
                return <div key={index} className="relative aspect-square">
                    <div className="w-full h-full bg-gray-200 animate-pulse"></div>
                </div>
            })}
        </div>
        <div className="flex items-center gap-4 text-sm text-gray-600">
            <Button variant="outline" className="flex items-center gap-1 cursor-pointer" onClick={() => { console.log('on click',); onMessageEdit(message) }}>
                重新编辑
            </Button>
            <Button variant="outline" className="flex items-center gap-1" onClick={() => onMessageGenerate(message)}>
                再次生成
            </Button>
        </div>

        {/* Image Viewer Modal */}
        {message.images && (
            <ImageViewer
                images={message.images}
                currentIndex={currentImageIndex}
                isOpen={imageViewerOpen}
                onClose={closeImageViewer}
                onNavigate={navigateImage}
            />
        )}
    </div>
}

const videoTypes = {
    'text2image': 'Text to Image',
    'image2image': 'Image to Image',
    'text2video': 'Text to Video',
    'image2video': 'Image to Video',
}

const imageRadios = {
    '1:1': '1:1',
    '16:9': '16:9',
    '4:3': '4:3',
}


export default function Dashboard() {
    // const [chat, setChat] = useState<Chat | null>(null);
    const { chat, setChat, setMessage } = useCurrentChatStore();
    const [messages, setMessages] = useState<Message[]>([]);
    const [prompt, setPrompt] = useState('');
    const [imageCount, setImageCount] = useState(1);
    const [type, setType] = useState('text2image');
    const [ratio, setRatio] = useState('1:1');
    const queryClient = useQueryClient()

    // 获取当前chat
    const { data: chatData } = useQuery({
        queryKey: ['currentChat'],
        queryFn: getCurrentChat,
    })

    useEffect(() => {
        if (chatData) {
            setChat(chatData);
        }
    }, [chatData, setChat])

    const { data: chatMessages } = useQuery({
        queryKey: ['chatMessages', chat?.id],
        queryFn: () => getChatMessages(chat?.id),
        refetchOnWindowFocus: false,
        enabled: !!chat?.id,
    })

    useEffect(() => {
        if (chatMessages) {
            setMessages(chatMessages)
        }
    }, [chatMessages, setMessage])

    // Poll for message completion status every 5 seconds
    const checkMessageStatus = useCallback(async (chatId: string, messageId: string) => {
        const result = await getChatMessage(chatId, messageId);
        if (result.status === 'processing') {
            // If still processing, check again in 5 seconds
            setTimeout(() => checkMessageStatus(chatId, messageId), 5000);
        } else {
            // Message is complete, update the message in chat
            const updatedMessages = messages?.map((msg: Message) =>
                String(msg.id) === messageId ? result : msg
            );
            setMessages(updatedMessages);

            removeStorage('message');
        }
    }, [messages])

    useEffect(() => {
        const message = getStorage('message');
        if (message) {
            const messageObj = JSON.parse(message);
            setMessage(messageObj);

            checkMessageStatus(chat.id, messageObj.id);
        }
    }, [chat.id, setMessage, checkMessageStatus])

    useEffect(() => {
        // 从服务器中获取最近的一次生成对象？一直保持用这一次的对象？
        console.log('chat', chat)
        // if (chat) {
        queryClient.invalidateQueries({ queryKey: ['chatMessages', chat.id] })
        // }
    }, [queryClient, chat])

    useEffect(() => {
        setParams({
            'type': type,
            'model': 'qwen-image',
            'size': ratio,
            'count': imageCount,
        })
    }, [imageCount, type, ratio])

    const [params, setParams] = useState({
        'type': 'text2image',
        'model': 'qwen-image',        // 模型类型， 如stable-diffusion, qwen-image, flux.dev
        'size': '1:1',
        'count': 1,
    });


    const onMessageGenerate = async () => {
        // 调用后台的api生成图片，然后图片以框架的方式显示
        let chatId = chat.id;
        if (!chatId) {
            const newChat = await createChat(prompt)
            setChat(newChat);
            chatId = newChat.id
        }

        const message = await createChatMessage(chatId, prompt, params);
        setMessage(message);

        // 将当前message的信息存入到strorge中，刷新的时候可以从storage中取出message信息，从而保持继续获取结果的处理
        setStorage('message', JSON.stringify(message));

        // 新增一个message
        const newMessages = [...messages, message];
        setMessages(newMessages);

        checkMessageStatus(chatId, message.id);
    }

    const onMessageEdit = (message: Message) => {
        setPrompt(message.prompt);
    }

    const onMessageReGenerate = async (message: Message) => {
        const chatId = chat.id;

        const prompt = message.prompt;
        const params = message.params;
        const newMessage = await createChatMessage(chatId, prompt, params);
        setMessage(newMessage);

        // 新增一个message
        const updatedMessages = [...messages, newMessage];
        setMessages(updatedMessages);
    }

    return <Layout>
        <LayoutBody className="flex flex-col justify-between">
            <div className="overflow-y-auto">
                {
                    messages?.map((message: Message) => (
                        <ChatMessage key={message.id} message={message} onMessageEdit={onMessageEdit} onMessageGenerate={onMessageReGenerate} />
                    ))
                }
            </div>

            <div className="">
                <div className="gap-4 border rounded-xl bg-gray-100 z-10">
                    <div className="flex items-center p-2">
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
                                        <span>{videoTypes[type as keyof typeof videoTypes]}</span>
                                        <IconChevronDown size={16} />
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent>
                                    {
                                        Object.entries(videoTypes).map(([key, value]) => {
                                            return <DropdownMenuItem key={key} onSelect={() => setType(key)}>
                                                {value}
                                            </DropdownMenuItem>
                                        })
                                    }
                                </DropdownMenuContent>
                            </DropdownMenu>

                            <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <Button variant="outline" className="gap-2 ml-2">
                                        <span>{imageRadios[ratio as keyof typeof imageRadios]}</span>
                                        <IconChevronDown size={16} />
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent>
                                    {
                                        Object.entries(imageRadios).map(([key, value]) => {
                                            return <DropdownMenuItem key={key} onSelect={() => setRatio(key)}>
                                                {value}
                                            </DropdownMenuItem>
                                        })
                                    }
                                </DropdownMenuContent>
                            </DropdownMenu>


                            <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <Button variant="outline" className="gap-2 ml-2">
                                        <span>{imageCount}</span>
                                        <IconChevronDown size={16} />
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent >
                                    {
                                        [1, 2, 3, 4].map((count) => (
                                            <DropdownMenuItem key={count} onSelect={() => setImageCount(count)}>
                                                {count}
                                            </DropdownMenuItem>
                                        ))
                                    }
                                </DropdownMenuContent>
                            </DropdownMenu>
                        </div>
                        <div className="flex items-center gap-2">
                            <Button onClick={onMessageGenerate}>Generate</Button>
                        </div>
                    </div>
                </div>
            </div>
        </LayoutBody>
    </Layout>
}