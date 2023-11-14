# Identify your Mac Scraper

Resolves model identifiers for model names from Apple's `Identify your model` pages. Primarily developed for syncing models when new Macs are released.

## Usage

Note Python 3.6+ is required, host agnostic.

```sh
pip3 -r requirements.txt
python3 scrape.py

# Alternate invocation for specific models(s)
python3 scrape.py 'MacBook' 'MacBook Air'
```

## Notes

- Apple's site is incomplete, generally stops around 2009 for Mac models
   - May also be missing models, ex. `MacBook5,1` is missing while `MacBook5,2` is present

## Sample

```json
{
    "MacBook": {
        "2017": {
            "MacBook10,1": [
                "MacBook (Retina, 12-inch, 2017)"
            ]
        },
        "..."
    },
    "MacBook Air": {
        "2023": {
            "Mac14,15": [
                "MacBook Air (15-inch, M2, 2023)"
            ]
        },
        "..."
    },
    "MacBook Pro": {
        "2023": {
            "Mac15,3": [
                "MacBook Pro (14-inch, Nov 2023)"
            ],
            "Mac15,6": [
                "MacBook Pro (14-inch, Nov 2023)"
            ],
            "..."
        },
        "..."
    },
    "iMac": {
        "2023": {
            "Mac15,5": [
                "iMac (24-inch, 2023)"
            ],
            "Mac15,4": [
                "iMac (24-inch, 2023)"
            ]
        },
        "..."
    },
    "Mac Pro": {
        "2023": {
            "Mac14,8": [
                "Mac Pro (2023)",
                "Mac Pro (Rack, 2023)"
            ]
        },
        "..."
    },
    "Mac Studio": {
        "2023": {
            "Mac14,13": [
                "Mac Studio (2023)"
            ],
            "Mac14,14": [
                "Mac Studio (2023)"
            ]
        },
        "..."
    },
    "Mac mini": {
        "2023": {
            "Mac14,3": [
                "Mac mini (2023)"
            ],
            "Mac14,12": [
                "Mac mini (2023)"
            ]
        },
        "..."
    }
}
```