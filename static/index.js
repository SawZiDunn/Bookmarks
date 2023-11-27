function goto(link) {
            if (!link.startsWith("http://") && !link.startsWith("https://")) {
                link = "https://" + link;
            }

            const newTab = window.open();
            newTab.location.href = link;
        }