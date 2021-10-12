import { escapeRegExp } from "@/api/utils";

export interface SocialMediaSite {
    site: string;
    url_format: string;
    icon: string;
    compiled_regex?: RegExp;
}

// compiles a regex which matches profile links for a given social media site
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

// tries to match a pasted URL with a particular social media site.
// if there is a match, returns a non-null Recognition object
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

// the return type of `tryRecogniseSocialLink`
export interface Recognition {
    site: SocialMediaSite;
    username: string;
}

// e.g.: for Facebook, will return
// a link of the form: https://www.facebook.com/[username-goes-here]
export function formatSocialLink(site: SocialMediaSite, username: string) {
    return site.url_format.replace("{username}", username);
}
