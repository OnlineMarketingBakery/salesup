# Blog field mapping (old PWR → salesup-theme HubL)

| Old PWR listing card | HubL (dynamic) |
|---|---|
| Post URL | `content.absolute_url` |
| Featured image | `content.featured_image` + `content.featured_image_alt_text` |
| Title | `content.name` |
| Teaser | `content.meta_description` or `content.post_list_content\|striptags\|truncatehtml(160)` |
| Date | `content.publish_date` |
| CTA | static label "Start met lezen" |

| Old PWR single | HubL (dynamic) |
|---|---|
| Title | `content.name` |
| Date | `content.publish_date` |
| Author | `content.blog_post_author.display_name` |
| Hero image | `content.featured_image` |
| Body (in-post CTAs) | `content.post_body` |
| Related (tag-based) | `{% related_blog_posts limit=3 %}` |
| Tags filter | `blog_tags(group.id, 250)` + `blog_tag_url(group.id, item.slug)` |
| Pagination | `next_page_num` + `blog_page_link(next_page_num)` |
