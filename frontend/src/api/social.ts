import { escapeRegExp } from "@/api/utils";

export interface SocialMediaSite {
    site: string;
    url_format: string;
    icon: string;
    compiled_regex?: RegExp;
}

export interface Recognition {
    site: SocialMediaSite;
    username: string;
}

function getRegexForSite(site: SocialMediaSite) {
    if (!site.compiled_regex) {
        let regexp = escapeRegExp(site.url_format).replace(
            "\\{username\\}",
            "([^/]+)\\/?"
        );
        site.compiled_regex = new RegExp(regexp);
    }
    return site.compiled_regex;
}

export function tryRecogniseSocialLink(
    sites: Map<string, SocialMediaSite>,
    link: string
): Recognition | null {
    for (let site of sites.values()) {
        let re = getRegexForSite(site);
        let result = re.exec(link);
        console.log(re, link, result);
        if (result !== null) {
            // we have a match
            return { site: site, username: result[1] };
        }
    }
    return null;
}

export function formatSocialLink(site: SocialMediaSite, username: string) {
    return site.url_format.replace("{username}", username);
}
