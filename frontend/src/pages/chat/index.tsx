import { useState, useEffect } from 'react';
import { Layout, LayoutBody } from '@/components/custom/layout'
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableFooter,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import type { Chat } from '@/store/chat'
import { getChats } from '@/api/chat'

export default function Chat() {
    const [page, setPage] = useState(1);
    const [chats, setChats] = useState<Chat[]>([]);

    useEffect(() => {
        const fetchChats = async () => {
            const result = await getChats(page, 10);
            console.log('fetch chats', result);
            setChats(result.items);
        }

        fetchChats();
    }, [page]);

    return <Layout>
        <LayoutBody className="flex flex-col justify-between">
            <Table>
                {/* <TableCaption>A list of your recent chats.</TableCaption> */}
                <TableHeader>
                    <TableRow>
                        <TableHead className="w-[100px]">No.</TableHead>
                        <TableHead>title</TableHead>
                        <TableHead>createdAt</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {chats.map((chat) => (
                        <TableRow key={chat.id}>
                            <TableCell className="font-medium"><a href={`/#/chats/${chat.id}`}>{chat.id}</a></TableCell>
                            <TableCell>{chat.title}</TableCell>
                            <TableCell>{chat.createdAt}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
                <TableFooter>
                    <TableRow>
                        {/* <TableCell colSpan={3}>Total</TableCell>
                        <TableCell className="text-right"></TableCell> */}
                    </TableRow>
                </TableFooter>
            </Table>
        </LayoutBody>
    </Layout >
}