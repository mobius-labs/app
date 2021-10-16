import { escapeRegExp } from "@/api/utils";

export interface SocialMediaSite {
    site: string;
    url_format: string;
    icon: string;
    compiledRegex?: RegExp;
}

// compiles a regex which matches profile links for a given social media site
function getRegexForSite(site: SocialMediaSite) {
    if (!site.compiledRegex) {
        const regexp = escapeRegExp(site.url_format).replace(
            "\\{username\\}",
            "([^/]+)\\/?"
        );
        site.compiledRegex = new RegExp(regexp);
    }
    return site.compiledRegex;
}

// the return type of `tryRecogniseSocialLink`
export interface Recognition {
    site: SocialMediaSite;
    username: string;
}

// tries to match a pasted URL with a particular social media site.
// if there is a match, returns a non-null Recognition object
export function tryRecogniseSocialLink(
    sites: Map<string, SocialMediaSite>,
    link: string
): Recognition | null {
    for (const site of sites.values()) {
        if (!site.url_format) {
            continue;
        }
        const re = getRegexForSite(site);
        const result = re.exec(link);
        console.log(re, link, result);
        if (result !== null) {
            // we have a match
            return { site: site, username: result[1] };
        }
    }
    return null;
}

// e.g.: for Facebook, will return
// a link of the form: https://www.facebook.com/[username-goes-here]
export function formatSocialLink(site: SocialMediaSite, username: string) {
    if (!site.url_format) {
        return username;
    }
    return site.url_format.replace("{username}", username);
}
