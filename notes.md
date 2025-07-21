
## Option 1

```
{     
    "Hierarchy": ["level_1"],
    "title": "level_1 - Some Header Text",
    "text": "some sample text"
}
{     
    "Hierarchy": ["level_1", "level_2"],
    "title": "level_2 - Some Header Text",
    "text": "some sample text"
}
{     
    "Hierarchy": ["level_1", "level_2", "level_3"],
    "title": "level_3 - Some Header Text",
    "text": "some sample text"
}
{     
    "Hierarchy": ["level_1", "level_2", "level_3", "level_4"]
    "title": "level_4 - Some Header Text"
    "text": "some sample text"
}
```
## Option 2

```
{     
    "title": "level_1 - Some Header Text",
    "text": "some sample text"
    "children: [
        {     
            "title": "level_2 - Some Header Text",
            "text": "some sample text"
            "children: [
                {     
                    "title": "level_3 - Some Header Text",
                    "text": "some sample text"
                    "children":[
                        {     
                            "title": "level_4 - Some Header Text"
                            "text": "some sample text"
                            "children":[]
                        }
                    ]
                }
            ]
        },
    ]
}

```
## Inputs to python script
hierarchy_keywords = ["Part", "Chapter", "Article", "Sec"]

## Desired JSON Structure
```
{
  "hierarchy": [],
  "title": "",
  "text": "",
  "tables": [],
  "images": []
}
```
Stormwater Design\nThis report summarizes the proposed system.\n\n## Key Components\n- Detention Basin\n- Inlet Control Structure\n- Overflow Weir\n\n**Note:** Final stabilization is required per EPD guidelines.
## Example HTML
```
Part 1 - Some Header Text 
<div class="chunk-content"> 
    Some content that is part of the Level_1 content block
</div>

Chapter 3 - Some Header Text 
<div class="chunk-content"> Some content that is part of the Chapter 3 content block
</div>

Article II - Some Header Text 
<div class="chunk-content"> Some content that is part of the Article II content block
</div>

Sec. 21. - Some Header Text 
<div class="chunk-content"> Some content that is part of the Sec. 21. content block
<table border="1" cellpadding="3" cellspacing="0" class="thead1 table left makeExpandableTable" rules="all" style="text-align:left;">
<colgroup class="std">
<col width="82.92682926829268%"/>
<col width="17.073170731707318%"/>
</colgroup>
    <thead>
        <th class="top">
        Type
        </th>
        <th class="top">
        Type2
        </th>
        <th class="top">
        Type3
        </th>
    </thead>
    <tbody>
        <tr>
            <td class="top">one</td>
            <td class="top">A</td>
            <td class="top">AA</td>
        </tr>
        <tr>
            <td class="top">two</td>
            <td class="top">C</td>
            <td class="top">CC</td>
        </tr>
        <tr>
            <td class="top">three</td>
            <td class="top">B</td>
            <td class="top">BB</td>
        </tr>
    </tbody>
</table>
</div>

Sec. 21.1 - Some Header Text 
<div class="chunk-content"> Some content that is part of the Sec. 21.1 content block
</div>

Sec. 21.2 - Some Header Text 
<div class="chunk-content"> Some content that is part of the Sec 21.2 content block
<a data-image-filename="produce1.png" href="https://mcclibrary.blob.core.usgovcloudapi.net/codecontent/14179/467533/produce1.png" target="_blank"><img alt="" data-image-filename="produce1.png" height="303" id="img_3" src="https://mcclibrary.blob.core.usgovcloudapi.net/codecontent/14179/467533/produce1.png" width="386"/></a>
</div>

Sec. 22. - Some Header Text 
<div class="chunk-content"> Some content that is part of the Sec. 22. content block
</div>

Sec. 22.1 - Some Header Text 
<div class="chunk-content"> Some content that is part of the Sec. 22.1 content block
</div>

Sec. 22.2 - Some Header Text 
<div class="chunk-content"> Some content that is part of the Sec 22.2 content block.

<table border="1" cellpadding="3" cellspacing="0" class="thead0 table left makeExpandableTable" rules="all" style="text-align:left;">
<colgroup class="std">
<col width="82.92682926829268%"/>
<col width="17.073170731707318%"/>
</colgroup>
    <tbody>
        <tr>
            <td class="top">House E&amp;S</td>
            <td class="top">$25.00</td>
        </tr>
        <tr>
            <td class="top">Pool E&amp;S</td>
            <td class="top">$15.00</td>
        </tr>
        <tr>
            <td class="top">Elevation Certificate</td>
            <td class="top">$35.00</td>
        </tr>
    </tbody>
</table>

Some more text.

<a data-image-filename="produce2.png" href="https://mcclibrary.blob.core.usgovcloudapi.net/codecontent/14179/467533/produce2.png" target="_blank"><img alt="" data-image-filename="produce2.png" height="303" id="img_3" src="https://mcclibrary.blob.core.usgovcloudapi.net/codecontent/14179/467533/produce2.png" width="386"/></a>
<a data-image-filename="produce3.png" href="https://mcclibrary.blob.core.usgovcloudapi.net/codecontent/14179/467533/produce3.png" target="_blank"><img alt="" data-image-filename="produce3.png" height="303" id="img_3" src="https://mcclibrary.blob.core.usgovcloudapi.net/codecontent/14179/467533/produce3.png" width="386"/></a>
</div>

Article III - Some Header Text 
<div class="chunk-content"> Some content that is part of the Article III content block
</div>

Sec. 31. - Some Header Text 
<div class="chunk-content"> Some content that is part of the Sec. 31. content block
<table border="1" cellpadding="3" cellspacing="0" class="thead1 table left makeExpandableTable" rules="all" style="text-align:left;">
<colgroup class="std">
<col width="82.92682926829268%"/>
<col width="17.073170731707318%"/>
</colgroup>
    <thead>
        <th class="top">
        Type
        </th>
        <th class="top">
        Type2
        </th>
        <th class="top">
        Type3
        </th>
    </thead>
    <tbody>
        <tr>
            <td class="top">one</td>
            <td class="top">A</td>
            <td class="top">AA</td>
        </tr>
        <tr>
            <td class="top">two</td>
            <td class="top">C</td>
            <td class="top">CC</td>
        </tr>
        <tr>
            <td class="top">three</td>
            <td class="top">B</td>
            <td class="top">BB</td>
        </tr>
    </tbody>
</table>
</div>
```

## Example Result

```
{     
    "Hierarchy": ["Part 1"],
    "title": "Part_1 - Some Header Text",
    "text": "Some content that is part of teh Level_1 content block"
},
{     
    "Hierarchy": ["Part 1", "Chapter 3"],
    "title": "Chapter 3 - Some Header Text",
    "text": "Some content that is part of the Chapter 3 content block",
},
{     
    "Hierarchy": ["Part 1", "Chapter 3", "Article II"],
    "title": "Article II - Some Header Text",
    "text": "Some content that is part of the Article II content block"
},
{     
    "Hierarchy": ["Part 1", "Chapter 3", "Article II", Sec. 21.]
    "title": "Sec. 21. - Some Header Text"
    "text": "Some content that is part of the Sec. 21. content block"
    "tables": [
        [
            {
                "Type": "one",
                "Type2": "A",
                "Type3": "AA"
            },
            {
                "Type": "two",
                "Type2": "C",
                "Type3": "CC"
            },
            {
                "Type": "three",
                "Type2": "B",
                "Type3": "BB"
            }
        ]
    ]
},
{     
    "Hierarchy": ["Part 1", "Chapter 3", "Article II", Sec. 21.1],
    "title": "Sec. 21.1 - Some Header Text",
    "text": "Some content that is part of the Article II content block"
    "images": [
        [
        "filename": "produce1.png"
        "src":"https://mcclibrary.blob.core.usgovcloudapi.net/codecontent/14179/467533/produce1.png"
        ]
    ]
},

{     
    "Hierarchy": ["Part 1", "Chapter 3", "Article II", Sec. 22],
    "title": "Part_1 - Some Header Text",
    "text": "Some content that is part of the Sec. 22. content block"
},
{     
    "Hierarchy": ["Part 1", "Chapter 3", "Article II", Sec. 22.1],
    "title": "Chapter 3 - Some Header Text",
    "text": "Some content that is part of the Sec. 22.1 content block,
},
{     
    "Hierarchy": ["Part 1", "Chapter 3", "Article II", Sec. 22.2],
    "title": "Article II - Some Header Text",
    "text": "Some content that is part of the Sec. 22.2 content block. Some more text"
    "tables": [
        [
        {
            "": "House E&S",
            "": "$25.00"
        },
        {
            "": "Pool E&S",
            "": "$15.00"
        },
        {
            "": "Elevation Certificate",
            "": "$35.00"
        }
        ]
    ]

    "images": [
        [
        "filename": "produce1.png"
        "src":"https://mcclibrary.blob.core.usgovcloudapi.net/codecontent/14179/467533/produce1.png"
        ]
        [
        "filename": "produce2.png"
        "src":"https://mcclibrary.blob.core.usgovcloudapi.net/codecontent/14179/467533/produce2.png"
        ]
        [
        "filename": "produce3.png"
        "src":"https://mcclibrary.blob.core.usgovcloudapi.net/codecontent/14179/467533/produce3.png"
        ]
    ]
},

{     
    "Hierarchy": ["Part 1", "Chapter 3", "Article III"],
    "title": "Article II - Some Header Text",
    "text": "Some content that is part of the Article II content block"
},
{     
    "Hierarchy": ["Part 1", "Chapter 3", "Article III", Sec. 31.]
    "title": "Sec. 31. - Some Header Text"
    "text": "Some content that is part of the Sec. 31. content block"
    "tables": [
        [
            {
                "Type": "one",
                "Type2": "A",
                "Type3": "AA"
            },
            {
                "Type": "two",
                "Type2": "C",
                "Type3": "CC"
            },
            {
                "Type": "three",
                "Type2": "B",
                "Type3": "BB"
            }
        ]
    ]
},

```


<table>
  <tr>
    <th rowspan="2">ZONING DISTRICT<br>Development Type</th>
    <th colspan="3">Minimum "Building Lot"</th>
    <th rowspan="2">Base Density<br>(Units/AC)</th>
    <th rowspan="2">Min. Open Space (I)</th>
    <th rowspan="2">Minimum Building Site (A)</th>
    <th rowspan="2">Minimum Street Frontage<br>Feet (M)</th>
    <th rowspan="2">Minimum Lot Width at Front Setback Line in Feet</th>
    <th rowspan="2">Minimum Lot Depth Average in Feet</th>
    <th rowspan="2">Minimum Floor Area<br>Sq. Ft. per Unit</th>
    <th rowspan="2">Maximum Impervious Area (B)(P)</th>
    <th colspan="3">Minimum Yard Setbacks</th>
    <th colspan="2">Maximum Structure Height (D)</th>
    <th rowspan="2">Minimum Zoning District Size</th>
  </tr>
  <tr>
    <th>Single-Family Structure</th>
    <th>Two-Family Structure</th>
    <th>Multi-family Structure & Max Units/AC</th>
    <th>Front in Feet (C)(O)</th>
    <th>Side in Feet</th>
    <th>Rear in Feet</th>
    <th>Stories</th>
    <th>Feet</th>
  </tr>
</table>


<table border="1" cellpadding="3" cellspacing="0" class="thead1 table left makeExpandableTable" rules="all" style="text-align:left;">
</colgroup>
    <thead>
        <th class="top">
        Type
        </th>
        <th class="top">
        Type2
        </th>
        <th class="top">
        Type3
        </th>
    </thead>
    <tbody>
        <tr>
            <td class="top">one</td>
            <td class="top">A</td>
            <td class="top">AA</td>
        </tr>
        <tr>
            <td class="top">two</td>
            <td class="top">C</td>
            <td class="top">CC</td>
        </tr>
        <tr>
            <td class="top">three</td>
            <td class="top">B</td>
            <td class="top">BB</td>
        </tr>
    </tbody>
</table>

<ol>
  <li>Submit permit application</li>
  <li>Conduct site inspection</li>
  <li>Receive approval</li>
</ol>

<ul>
  <li>Stormwater report</li>
  <li>Soil erosion plan</li>
  <li>Site layout</li>
</ul>

<ol type="A" start="3">
    <li>Item C</li>
    <li>Item D</li>
    <li>Item E</li>
</ol>


## Before modifying 
<p class="incr1"> 1. <\p>
<p class="content2"> 1 content<\p>
<p class="incr2"> a <\p>
<p class="content3"> a content <\p>
<p class="incr2"> b <\p>
<p class="content3"> b content <\p>
<p class="incr1"> 2. <\p>
<p class="content2"> 2 content <\p>

## Desired Output
<ol type="1" start="1">
    <li>Some content.
        <ol type="a">
            <li>a content</li>
            <li>b content</li>
        </ol>
    </li>
    <li>2 content</li>
</ol>
