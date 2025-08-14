import { useEffect, useMemo, useCallback } from "react"
import { BadgeDollarSign } from "lucide-react"
import { IconChevronDown, IconX, IconChevronUp, IconChevronDown as IconChevronDownIcon } from '@tabler/icons-react'
import { useQueryClient, useQuery } from '@tanstack/react-query'
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu'
import { Layout, LayoutBody } from '@/components/custom/layout'
import { Textarea } from '@/components/ui/textarea'
import { useCurrentChatStore } from '@/store/chat'
import type { Image, Message } from '@/store/chat'
import { createChat, createChatMessage, getChatMessage, getChatMessages, getCurrentChat } from '@/api/chat'
import { getUserCredits } from '@/api/credit'
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { getStorage, setStorage, removeStorage } from '@/storage'
import { useToast } from '@/hooks/use-toast'
import { ApiResponseWrapper } from '@/lib/api'
import { CreditInfo } from '@/components/credit-info'

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
    // Add ESC key listener
    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                onClose();
            }
        };

        if (isOpen) {
            document.addEventListener('keydown', handleKeyDown);
        }

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [isOpen, onClose]);

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
                        <IconChevronUp className="w-4 h-4" />
                    </Button>
                    <Button
                        variant="ghost"
                        size="icon"
                        className={`bg-white/20 hover:bg-white/30 text-white ${!hasNext ? 'opacity-50 cursor-not-allowed' : ''}`}
                        onClick={() => hasNext && onNavigate('next')}
                        disabled={!hasNext}
                    >
                        <IconChevronDownIcon className="w-4 h-4" />
                    </Button>
                </div>

                {/* Main image */}
                <img
                    src={currentImage.imageUrl}
                    alt={`Image ${currentIndex + 1}`}
                    className="max-w-full max-h-full object-contain"
                />

                {/* Image counter */}
                <div className="absolute bottom-4 left-1/2 transform -translate-y-1/2 bg-black/50 text-white px-3 py-1 rounded-full text-sm">
                    {currentIndex + 1} / {images.length}
                </div>
            </div>
        </div>
    );
};

const ChatMessage = ({ message, onMessageEdit, onMessageGenerate }: { message: Message, onMessageEdit: (message: Message) => void, onMessageGenerate: (message: Message) => void }) => {

    // 确保placeholder数量正确，优先使用message.count，如果没有则使用params中的count
    const placeholderCount = message.count || (message.params?.count || 1);
    const placeholderImages = useMemo(() => Array(placeholderCount).fill(0), [placeholderCount]);
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
        {/* Debug info - remove in production */}
        <div className="text-xs text-gray-400 mb-2">
            Count: {placeholderCount}, Status: {message.status}, Images: {message.images?.length || 0}
        </div>
        <div className={`grid gap-2 p-2 ${message.images && message.images.length > 0
            ? (message.images.length === 1 ? 'grid-cols-1' : message.images.length === 2 ? 'grid-cols-2' : message.images.length === 3 ? 'grid-cols-3' : 'grid-cols-4')
            : (placeholderCount === 1 ? 'grid-cols-1' : placeholderCount === 2 ? 'grid-cols-2' : placeholderCount === 3 ? 'grid-cols-3' : 'grid-cols-4')
            }`}>
            {message.images && message.images.length > 0 ? (
                // Show actual images when available
                message.images.map((image: Image, index: number) => (
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
                ))
            ) : (
                // Show placeholder images based on count
                placeholderImages.map((_, index) => (
                    <div key={index} className="relative aspect-square">
                        <div className="w-full h-full bg-gray-200 animate-pulse rounded-lg flex items-center justify-center">
                            {message.status === 'running' || message.status === 'processing' || message.status === 'pending' ? (
                                <div className="w-8 h-8 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
                            ) : (
                                <div className="w-8 h-8 border-4 border-gray-300 border-t-gray-400 rounded-full animate-pulse"></div>
                            )}
                        </div>
                    </div>
                ))
            )}
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
        {message.images && message.images.length > 0 && (
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

const modelTypes = {
    'qwen-image': 'Qwen Image',
    'flux1.dev': 'Flux1.dev',
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
    const [imageCount, setImageCount] = useState(4);
    const [type, setType] = useState('text2image');
    const [model, setModel] = useState('qwen-image');
    const [ratio, setRatio] = useState('1:1');
    const [isGenerating, setIsGenerating] = useState(false);
    const queryClient = useQueryClient()
    const { toast } = useToast()

    // 获取当前chat
    const { data: chatData } = useQuery({
        queryKey: ['currentChat'],
        queryFn: getCurrentChat,
    })

    // 获取用户credit信息
    const { data: creditInfo } = useQuery({
        queryKey: ['userCredits'],
        queryFn: getUserCredits,
        refetchOnWindowFocus: false,
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
        try {
            console.log(`🔍 Checking status for message ${messageId} in chat ${chatId}...`);
            console.log(`📡 Making API call to: /chats/${chatId}/messages/${messageId}`);

            const result = await getChatMessage(chatId, messageId);
            console.log(`✅ API response received:`, result);
            console.log(`📊 Message ${messageId} status:`, result.status, 'Images:', result.images?.length);

            // Check if the result has a status property and it's still processing
            if (result && result.status && (result.status === 'processing' || result.status === 'running' || result.status === 'pending')) {
                console.log(`⏳ Message ${messageId} still processing (status: ${result.status}), checking again in 5 seconds...`);
                // If still processing, check again in 5 seconds
                setTimeout(() => {
                    console.log(`🔄 Scheduling next check for message ${messageId}...`);
                    checkMessageStatus(chatId, messageId);
                }, 5000);
            } else {
                console.log(`🎉 Message ${messageId} completed with status:`, result.status);
                // Message is complete, update the message in chat
                setMessages(prevMessages => {
                    const updatedMessages = prevMessages?.map((msg: Message) =>
                        String(msg.id) === messageId ? result as Message : msg
                    );
                    console.log(`📝 Updated messages array:`, updatedMessages);
                    return updatedMessages;
                });

                // Reset generating state when complete
                setIsGenerating(false);
                removeStorage('message');

                console.log(`✅ Message ${messageId} updated successfully, images count:`, result.images?.length);
            }
        } catch (error) {
            console.error(`❌ Error checking message status for ${messageId}:`, error);
            console.error(`🔍 Error details:`, {
                chatId,
                messageId,
                error: error.message,
                stack: error.stack
            });
            // If there's an error, try again in 5 seconds
            setTimeout(() => {
                console.log(`🔄 Retrying status check for message ${messageId} after error...`);
                checkMessageStatus(chatId, messageId);
            }, 5000);
        }
    }, []) // 移除messages依赖

    useEffect(() => {
        const message = getStorage('message');
        if (message && chat?.id) {
            const messageObj = JSON.parse(message);
            setMessage(messageObj);

            checkMessageStatus(chat.id, messageObj.id);
        }
    }, [chat?.id, setMessage, checkMessageStatus])

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
            'model': model,
            'size': ratio,
            'count': imageCount,
        })
    }, [imageCount, type, ratio, model])

    const [params, setParams] = useState({
        'type': 'text2image',
        'model': 'qwen-image',        // 模型类型， 如stable-diffusion, qwen-image, flux.dev
        'size': '1:1',
        'count': 1,
    });

    // Test function to verify API calls
    const testApiCall = async (chatId: string, messageId: string) => {
        try {
            console.log(`🧪 Testing API call to getChatMessage...`);
            console.log(`🔗 URL: ${import.meta.env.VITE_PUBLIC_API_URL}/chats/${chatId}/messages/${messageId}`);

            const result = await getChatMessage(chatId, messageId);
            console.log(`✅ Test API call successful:`, result);
            return true;
        } catch (error) {
            console.error(`❌ Test API call failed:`, error);
            return false;
        }
    };

    const onMessageGenerate = async () => {
        if (!prompt.trim() || isGenerating) return;

        console.log(`🚀 Starting image generation process...`);
        console.log(`📝 Prompt:`, prompt);
        console.log(`⚙️ Params:`, params);

        // Set generating state
        setIsGenerating(true);
        console.log(`⏳ Set generating state to true`);

        try {
            // 调用后台的api生成图片，然后图片以框架的方式显示
            let chatId = chat?.id;
            if (!chatId) {
                console.log(`💬 No existing chat, creating new chat...`);
                const newChat = await createChat(prompt)
                console.log(`✅ New chat created:`, newChat);
                setChat(newChat);
                chatId = newChat.id
            } else {
                console.log(`💬 Using existing chat:`, chatId);
            }

            console.log(`📡 Creating chat message with chatId: ${chatId}`);
            const message = await createChatMessage(chatId, prompt, params);
            console.log(`✅ Message created:`, message);
            setMessage(message as Message);

            // 将当前message的信息存入到strorge中，刷新的时候可以从storage中取出message信息，从而保持继续获取结果的处理
            setStorage('message', JSON.stringify(message));
            console.log(`💾 Message saved to storage`);

            // 新增一个message
            const newMessages = [...messages, message as Message];
            setMessages(newMessages);
            console.log(`📝 Messages array updated, total messages:`, newMessages.length);

            // Clear prompt input
            setPrompt('');
            console.log(`🧹 Prompt input cleared`);

            // Test API call first
            console.log(`🧪 Testing API call before starting polling...`);
            const apiTestResult = await testApiCall(chatId, message.id);

            if (apiTestResult) {
                console.log(`🔄 Starting status check for message: ${message.id} in chat: ${chatId}`);
                // 确保轮询立即开始
                setTimeout(() => {
                    console.log(`⏰ Executing delayed status check for message: ${message.id}`);
                    checkMessageStatus(chatId, message.id);
                }, 100);
            } else {
                console.error(`❌ API test failed, cannot start polling`);
            }

        } catch (error) {
            console.error('Error creating message:', error);

            // 处理不同类型的错误
            if (error.status === 'limit') {
                // Credit不足或达到限制
                toast({
                    variant: "limit",
                    title: "Credit Limit Reached",
                    description: error.message || "You don't have enough credits to generate images. Please purchase a subscription plan.",
                });
            } else if (error.status === 'error') {
                // 其他错误
                toast({
                    variant: "destructive",
                    title: "Error",
                    description: error.message || "Failed to create message. Please try again.",
                });
            } else {
                // 未知错误
                toast({
                    variant: "destructive",
                    title: "Unknown Error",
                    description: "An unexpected error occurred. Please try again.",
                });
            }
        } finally {
            // Reset generating state
            setIsGenerating(false);
            console.log(`⏳ Reset generating state to false`);
        }
    }

    const onMessageEdit = (message: Message) => {
        setPrompt(message.prompt);
    }

    const onMessageReGenerate = async (message: Message) => {
        const chatId = chat?.id;
        if (!chatId) return;

        const prompt = message.prompt;
        const params = message.params;
        const newMessage = await createChatMessage(chatId, prompt, params);
        console.log('Re-generated message:', newMessage);
        setMessage(newMessage as Message);

        // 新增一个message
        const updatedMessages = [...messages, newMessage as Message];
        setMessages(updatedMessages);

        // 启动状态轮询
        console.log('Starting status check for re-generated message:', newMessage.id, 'in chat:', chatId);
        // 确保轮询立即开始
        setTimeout(() => {
            checkMessageStatus(chatId, newMessage.id);
        }, 100);
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

            <div className="flex gap-4">
                {/* Credit信息侧边栏 */}
                {/* <div className="w-80 flex-shrink-0">
                    <CreditInfo
                        balance={creditInfo?.balance || 0}
                        imagesRemaining={creditInfo?.imagesRemaining || 0}
                        canGenerate={creditInfo?.canGenerate || false}
                        onUpgrade={() => {
                            toast({
                                title: "Upgrade Plan",
                                description: "Redirecting to subscription page...",
                            });
                            // TODO: 实现跳转到订阅页面
                        }}
                    />
                </div> */}

                {/* 主要的输入区域 */}
                <div className="flex-1">
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
                                {/* <DropdownMenu>
                                    <DropdownMenuTrigger asChild>
                                        <Button variant="outline" className="gap-2" disabled={isGenerating}>
                                            <span>{modelTypes[model as keyof typeof modelTypes]}</span>
                                            <IconChevronDown size={16} />
                                        </Button>
                                    </DropdownMenuTrigger>
                                    <DropdownMenuContent>
                                        {
                                            Object.entries(modelTypes).map(([key, value]) => {
                                                return <DropdownMenuItem key={key} onSelect={() => setModel(key)}>
                                                    {value}
                                                </DropdownMenuItem>
                                            })
                                        }
                                    </DropdownMenuContent>
                                </DropdownMenu>

                                <DropdownMenu>
                                    <DropdownMenuTrigger asChild>
                                        <Button variant="outline" className="gap-2" disabled={isGenerating}>
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
                                </DropdownMenu> */}

                                <DropdownMenu>
                                    <DropdownMenuTrigger asChild>
                                        <Button variant="outline" className="gap-2 ml-2" disabled={isGenerating}>
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
                                        <Button variant="outline" className="gap-2 ml-2" disabled={isGenerating}>
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
                                <Button
                                    onClick={onMessageGenerate}
                                    disabled={!prompt.trim() || isGenerating || !creditInfo?.canGenerate}
                                    className={!prompt.trim() || isGenerating || !creditInfo?.canGenerate ? 'opacity-50 cursor-not-allowed' : ''}
                                >
                                    {isGenerating ? 'Generating...' : 'Generate'}
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </LayoutBody>
    </Layout>
}