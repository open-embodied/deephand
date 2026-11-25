### Open Source DeepHand Hand Communication Board



This folder contains the production files, source files, and reference documents for the Communication PCB used in the open-source DeepHand Hand project. The board was designed in Altium Designer, and the files are provided to allow users to review, modify, and manufacture the PCB.



#### Included files



1\. Source\_File.zip

&#x20;  This zip file contains the editable Altium Designer source files for the PCB design. Users who want to modify the schematic or PCB layout should use the files in this folder. There are also ASCII files for schematic and PCB layout.



2\. Communication\_Schematic.pdf

&#x20;  PDF version of the circuit schematic. This file can be used to understand the circuit design, check connections, and debug the board.



3\. Assembly\_Top.PDF

&#x20;  Top-side assembly drawing of the PCB. This file shows the component locations and reference designators on the top side of the board. We only have top assembly for this board.



4\. BOM\_Communication.csv

&#x20;  Bill of Materials (BOM) for the PCB. This file lists the components used in the design and is required for PCB assembly.



5\. CPL\_Communication.csv

&#x20;  Pick-and-place file, also known as the CPL file. This file contains the component position, rotation, and layer information required for automated PCB assembly.



6\. Gearber\_Drill.zip

&#x20;  Gerber and drill files for PCB fabrication. This ZIP file can be uploaded directly to JLCPCB for bare PCB production.



7\. Communication\_3D.pdf

&#x20;  3D PDF preview of the PCB. This file can be used to visually inspect the board layout and component placement.



8\. Communication.step

&#x20;  STEP 3D model of the PCB assembly. This file can be imported into CAD software for mechanical integration and enclosure/robotic hand assembly checks.



#### How to order from JLCPCB

1\. Go to JLCPCB order page: https://cart.jlcpcb.com/quote?spm=jlcpcb.Public.2006



2\. Upload the Gerber and drill ZIP file:

&#x20;  - Gerber\_Drill.zip

&#x20;  The website will process the file and show you the top and bottom side of the PCB.



3\. Check the Gerber preview carefully. Make sure the board outline, holes, copper layers, solder mask, and silkscreen look correct.



4\. Select the PCB manufacturing options, such as:

&#x20;  - Base Material: FR-4 (default)

&#x20;  - Layers and dimensions should be updated automatically

&#x20;  - PCB thickness: 1.6mm

&#x20;  - Copper weight: 1oz

&#x20;  - Via covering: Tented 

&#x20;  - You can leave other options default or change based on your need



5\. If you only want to order bare PCBs, you can continue directly to checkout after confirming the PCB settings.



6\. If you want to order assembled PCBs, enable PCB assembly / SMT assembly.

&#x20;  - You can use the default setting in PCB Assembly and Advanced Options or change based on your need.



7\. Upload the Bill of Materials file and CPL file:

&#x20;  - BOM\_Communication.csv

&#x20;  - CPL\_Communication.csv



8\. Check the component matching results.

&#x20;  Make sure the selected components match the intended values, footprints, and package types. (If any parts are sold out, you can pre-order the part in JLC Parts)



9\. Check the assembly preview. For KW30-3S-1H(800), the footprint is not available in EasyEDA so it won't show in the preview page.



10\. Review the final order summary, including PCB fabrication, assembly, components, quantity, and shipping. And now it's ready to place the order.



#### License

The hardware design files are released under the CERN Open Hardware Licence Version 2 - Permissive (CERN-OHL-P v2), unless otherwise stated.

