import {API_HOST} from "@/config";

export async function getSitePages() {
    let response = await fetch(`${API_HOST}/pages/site.json`)
    let data = await response.json()


}
