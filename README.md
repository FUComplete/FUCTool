
<div align="center">

![FUCToolHeader](https://user-images.githubusercontent.com/5410031/222875778-cfe3a997-42aa-4b97-a038-edaf6b29e1ce.png)

<hr>

<img src="https://user-images.githubusercontent.com/5410031/222876293-c91e184a-ca66-4491-9208-5aa7b46c045d.png" width="25%"></img><img src="https://user-images.githubusercontent.com/5410031/222876408-a713c9de-6a49-4e6c-a34e-f98f24ecfaf2.png" width="25%"></img><img src="https://user-images.githubusercontent.com/5410031/222877070-d66314a7-526a-4428-9254-ac5b6097bbc3.png" width="25%"></img><img src="https://user-images.githubusercontent.com/5410031/222877120-dc203fa8-f929-40b9-a5ed-65360f637c66.png" width="25%"></img>  
<hr>

### <ins>What is FUCTool?</ins>

</div>

FUCTool is an application to install and manaage various settings and options of the FUComplete patch. As of latest release, it is bundled with the patch. This repo is for more detailed information and source to the tool. 

The tool is split into 4 sections:

* [Patcher](#patcher)
* [Configuration](#configuration)
* [File Replacer](#file-replacer)
* [Custom Quests](#custom-quests)

<div align="center">
<h2>Patcher</h2>
</div>

Make sure you use either a UMD dump or PSN version of `Monster Hunter Portable 2nd G`.

Press the `Select` button to select your ISO.

In the output window you should see:
  ``` 
  INFO | Checking ISO...
  INFO | Valid ISO file.
  ```
If instead you get:
  ```
  INFO | Checking ISO...
  ERROR | Invalid ISO, your dump should match one of the following md5 hashes:
  ERROR | UMD: 1f76ee9ccbd6d39158f06e6e5354a5bd
  ERROR | PSN: cc39d070b2d2c44c9ac8187e00b75dc4
  ```
Please make sure you select the correct image that matches the above hashes.

Check `Keep patched DATA.BIN outside of the ISO.` if you plan to modify files and use file replacer. See [File Replacer](#file-replacer) for more information on how to use this feature and what can be done.

Press the `Patch ISO` button to start the patching process. You'll know its done once you see `INFO | Patching done`

<div align="center">

| <img src="https://user-images.githubusercontent.com/5410031/221740339-9e2baf45-cfba-4798-af37-4a819f0d24d3.png" width="50%"></img> |
|:---:|
| Patching Completed |

</div>

<div align="center">
<h2>Configuration</h2>
</div>

The `Configuration` tab handles setting the various options and features of the patch.

### <ins>`File Replacer Path`</ins>

Sets where `nativePSP` should be read from, either `DISC0` or `MS0`.

When set to `DISC0`, it loads `nativePSP` from the ISO. Currently the only files internally are Dos battle themes. When set to `MS0`, it loads `nativePSP` from the `ms0:/FUC/` directory. 
#### **Note:** if you set it to `MS0`, please extract the numbered files from the ISO and place them in the `ms0:/FUC/nativePSP` directory.

```
.
├───FUC
│   │   config.bin
│   │   loader.bin
│   │
│   └───nativePSP
│           6552 <──────┐
│           6553        │
│           6554        ├──── These files.
│           6555        │
│           6566        │
│           6571 <──────┘
│           file.bin
│
└───PSP_GAME
```

For more information on how to use this feature fully, please see the [File Replacer](#file-replacer) section.

**Default is `DISC0`**

### <ins>`Save Region`</ins>

Sets what region save should be loaded, so you can continue using your existing save with the patch.

* `ULJM05500` - Monster Hunter Portable 2nd G (JP) save
* `ULUS10391` - Monster Hunter Freedom Unite (NA) save
* `ULES01213` - Monster Hunter Freedom Unite (EU) save

**Default is `ULUS10391`**

### <ins>`True Raw/Ele/Status Display`</ins>

"Debloats" the modifiers on weapons to display their true raw, element and status values. 

| <img src="https://user-images.githubusercontent.com/5410031/222886750-84076286-73e1-4345-85f2-74ca51c48129.png" width="75%"></img> | <img src="https://user-images.githubusercontent.com/5410031/222886753-37f37ed4-e0b8-4cb0-b3f6-be4db872f57e.png" width="75%"></img> |
|:---:|:---:|
| Disabled | Enabled |

This is purely visual and removes the need to calculate the true values of a weapon.

**Default is `Disable`**

### <ins>`Dos Audio`</ins>

Replaces various battle themes with their Dos counterparts. These themes are:

* [Jungle](https://youtu.be/wP1Tiq74gWs)
* [Desert](https://youtu.be/Hjf1QfiTBbY)
* [Swamp](https://youtu.be/ZRQT-QYB0_I)
* [Snowy Mountain](https://youtu.be/7T0Vp7okMhE)
* [Volcano](https://youtu.be/vHSCNxTjX1c)
* [Tower](https://youtu.be/f5ZNBm9EuEc)

**Default is `Disable`**

### <ins>`Field of View`</ins>

Allows adjusting how much of the games "world" you can see.

| <img src="https://user-images.githubusercontent.com/5410031/222886598-b0b1aa84-ba61-4a57-a19c-e567869e0065.png"></img> | <img src="https://user-images.githubusercontent.com/5410031/222886632-1df51f5c-d92f-46fb-a5d4-9dbf831d753f.png"></img> | <img src="https://user-images.githubusercontent.com/5410031/222886645-173cdf74-96b3-4b53-87f0-05cfabef1105.png"></img> | <img src="https://user-images.githubusercontent.com/5410031/222886655-d1dbcd29-0991-49b8-b208-ed79b6f83804.png"></img> |
|:---:|:---:|:---:|:---:|
| Default | Minor | Moderate | Extreme |

**Default is `Default`**

### <ins>`Starting Vertical Camera Position`</ins>

Sets the starting vertical camera position when you embark on a quest.

| <img src="https://user-images.githubusercontent.com/5410031/222885440-e3673dfd-638f-4466-96b9-454848f9b5ec.png"></img> | <img src="https://user-images.githubusercontent.com/5410031/222885447-0d2cb33d-6b9c-48f4-9b1e-fffc57a07581.png"></img> | <img src="https://user-images.githubusercontent.com/5410031/222885451-08607fa6-8e17-40ca-b2dd-1e878aac45e6.png"></img> | <img src="https://user-images.githubusercontent.com/5410031/222885457-bd514106-25be-4fe7-8c94-5954f68a0b51.png"></img> | <img src="https://user-images.githubusercontent.com/5410031/222885461-9147372c-ceb6-43ce-a327-babc7d65c777.png"></img> |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 2 | 3 | 4 | 5 |

**Default is `4 (Default)`**

### <ins>`Minimap Size`</ins>

Sets a scaling modifier for minimap size. If either `75%` or `50%` are selected the loading screen map is also scaled down.

| <img src="https://user-images.githubusercontent.com/5410031/222886134-5a1496b0-3dfc-422d-958d-fc8696caff16.png"></img> | <img src="https://user-images.githubusercontent.com/5410031/222886139-a050a54c-ba83-4d91-bd13-9ac3b74ccd90.png"></img> | <img src="https://user-images.githubusercontent.com/5410031/222886143-4abfa86e-673b-4876-8214-03382a696f37.png"></img> |
|:---:|:---:|:---:|
| Default | 75% | 50% |

**Default is `Default`**

### <ins>`Hunting Horn Tweak`</ins>

Enable/Disable modified Hunting Horn mechanics. When disabled, you have vanilla hunting horn values/mechanics however when enabled you have:

* Note mechanics work similar to Frontier, where notes only clear if you sheath your weapon or have a forced sheathed interaction.
* Left and right swing MV/KO values increased to match P2/F2 values. 31 MV and 18 KO, up from 27 MV and 15 KO.
* Hilt jab poke attack now does cutting damage instead of impact.

**Default is `Disable`**


## File Replacer

TBD

## Custom Quests

`Custom Quests` tab allows you to backup and inject custom quests into your save. Up to 18 quests can be injected and it supports both `.pat` and `.mib` *(decrypted)*.

To use, place your `.pat` or `.mib` quests in the `quests` folder. Press the `Select` button and open the folder containing `MHP2NDG.BIN` (example: `ms0:/PSP/SAVEDATA/ULUS10391`)

When the save is loaded, you have a few options:

* To backup, select the quests that you wish to backup in the right pane and press the `<---` button. This will backup the quests to the `quests` folder with the extension `.mib.dec`.
  - **Note:** You can backup challenge quests however you can **NOT** write them back to the save.
* To delete/make room for new quests, highlight the ones you wish to remove and press the `Remove` button.
* To add, select the quests in the left pane (up to 18) and press the `--->` button to inject them into your save.
  - If you added quests to the `quests` folder and dont see them in the left pane, you may have to press the `Rescan folder` button or the quests are encrypted. If the quests are encrypted please decrypt them first.

Once you are happy, press the `Save` button to write the changes.

You may see a message like this pop-up on PPSSPP.

<div align="center">

![saveprompt](https://user-images.githubusercontent.com/5410031/224438314-5c00cd43-c849-4b00-998c-4d7dafb51dfb.png)

</div>

If you do, you can remove it by saving in-game and you'll no longer see the message.

To play your custom quests, go to the guildhall, open your options menu and under `Savedata Quests` toggle the option `ON`. Once enabled talk to a quest giver and open the "Events" tab... you should see your injected quests.

| <img src="https://user-images.githubusercontent.com/5410031/224439333-98330920-1cad-4dc6-9fdf-8fff490f5d1b.png" width="75%"></img> | <img src="https://user-images.githubusercontent.com/5410031/224439336-f390867f-08d0-40e3-bab5-a8b04ca80f8e.png" width="75%"></img> |
|:---:|:---:|
| Options Menu | Injected Quests |
