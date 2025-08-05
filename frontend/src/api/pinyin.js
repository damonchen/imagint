import { appApi } from '@/lib/api'

export async function getPinyin(hanzi) {
    return appApi.put('pinyin', {hanzi})
}
