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

- Apple's site is incomplete, generally stops around 2009 for Mac models.
   - May also be missing models, ex. `MacBook5,1` is missing while `MacBook5,2` is present.
   - Known missing models:
     - MacBook5,1
     - MacBookPro5,4
     - iMac11,1
     - iMac13,3
     - iMac14,3
     - Macmini5,3
- iMac Pro is part of the iMac family, thus is not listed separately.
- Some models, ex. `MacBookPro11,3`, may appear in multiple years with different model names.
  - 2013: `MacBook Pro (Retina, 15-inch, Late 2013)`
  - 2014: `MacBook Pro (Retina, 15-inch, Mid 2014)`
- For the 2023 MacBook Air, Mac15,2 is a typo (should be Mac15,12)
- Current URLs indexed:
  - [MacBook - HT201608](https://support.apple.com/HT201608)
  - [MacBook Air - HT201862](https://support.apple.com/HT201862)
  - [MacBook Pro - HT201300](https://support.apple.com/HT201300)
  - [iMac - HT201634](https://support.apple.com/HT201634)
  - [Mac Pro - HT202888](https://support.apple.com/HT202888)
  - [Mac Studio - HT213073](https://support.apple.com/HT213073)
  - [Mac mini - HT201894](https://support.apple.com/HT201894)
- As noted by Eric Boyd from Apple, localization may 2 weeks to update. US English will always be the most up-to-date.
  - Project currently defaults to `en-us`, edit scrape.py's `LOCALIZATION` variable to change this.


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