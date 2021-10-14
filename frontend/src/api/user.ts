import { getAxiosInstance } from "@/api/api";

export interface User {
    email: string;
    business_card: boolean;
}

export async function fetchUserDetails(): Promise<User> {
    const result = await getAxiosInstance().get(
        "/account/get_business_card_visibility"
    );
    return result.data as User;
}
