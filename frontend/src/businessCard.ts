import { User } from "@/api/user";

export const CARD_THEMES = {
    default: {
        label: "White Smoke",
    },
    dark: {
        label: "Graphite Night",
    },
    sky: {
        label: "Clear Sky",
    },
    bright: {
        label: "Tropical Light",
    },
};

export function getTheme(user: User | null): string {
    if (!user || !user.business_card_theme) {
        return "default";
    }
    return user.business_card_theme;
}
