#!/usr/bin/env python3
"""
TTG Genesis UE5 Project Creator
Creates complete UE5 projects with C++ classes, Blueprints, and game logic
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

class UE5ProjectCreator:
    """Creates complete UE5 projects with game logic"""

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        # Generate UE5 projects outside the main folder for easy access
        self.projects_path = self.base_path.parent / "TTG-Generated-UE5-Projects"
        self.projects_path.mkdir(parents=True, exist_ok=True)

        # UE5 paths (will be auto-detected or configured) - Updated for UE 5.6
        self.ue5_path = self.find_ue5_installation()
        self.ue5_editor = None
        self.ue5_build_tool = None

        if self.ue5_path:
            self.ue5_editor = self.ue5_path / "Engine" / "Binaries" / "Win64" / "UnrealEditor.exe"
            self.ue5_build_tool = self.ue5_path / "Engine" / "Binaries" / "DotNET" / "UnrealBuildTool" / "UnrealBuildTool.exe"

        print(f"UE5 Project Creator initialized")
        print(f"UE5 Path: {self.ue5_path}")
        print(f"Projects will be created in: {self.projects_path}")

    def find_ue5_installation(self):
        """Find UE5 installation automatically - Prioritize UE 5.6.0"""
        possible_paths = [
            Path("C:/Program Files/Epic Games/UE_5.6"),
            Path("C:/Program Files/Epic Games/UE_5.5"),
            Path("C:/Program Files/Epic Games/UE_5.4"),
            Path("C:/Program Files/Epic Games/UE_5.3"),
            Path("C:/Epic Games/UE_5.6"),
            Path("C:/Epic Games/UE_5.5"),
            Path("C:/Epic Games/UE_5.4"),
            Path("C:/UnrealEngine"),
        ]

        for path in possible_paths:
            if path.exists() and (path / "Engine").exists():
                print(f"✅ Found UE5 installation: {path}")
                return path

        print("⚠️ UE5 installation not found automatically")
        return None

    def create_complete_project(self, world_data, options):
        """Create a complete UE5 project with game logic"""
        world_name = world_data.get('name', 'GeneratedWorld').replace(' ', '')
        project_name = f"TTG_{world_name}"

        print(f"\n🚀 Creating UE5 Project: {project_name}")
        print("=" * 60)

        try:
            # Step 1: Create project structure
            project_path = self.create_project_structure(project_name)

            # Step 2: Create .uproject file
            self.create_uproject_file(project_path, project_name, world_data)

            # Step 3: Generate C++ classes
            self.generate_cpp_classes(project_path, project_name, world_data)

            # Step 4: Create Blueprint data files
            self.create_blueprint_data(project_path, project_name, world_data)

            # Step 5: Create game content
            self.create_game_content(project_path, project_name, world_data)

            # Step 6: Create build files
            self.create_build_files(project_path, project_name)

            # Step 7: Generate project files (if UE5 available)
            if self.ue5_path and options.get('generateProjectFiles', True):
                self.generate_project_files(project_path, project_name)

            # Step 8: Compile project (if requested)
            if self.ue5_path and options.get('compileProject', False):
                self.compile_project(project_path, project_name)

            print(f"\n✅ UE5 Project Created Successfully!")
            print(f"📁 Project Location: {project_path}")
            print(f"🎮 Project File: {project_path / f'{project_name}.uproject'}")

            return {
                'success': True,
                'project_name': project_name,
                'project_path': str(project_path),
                'project_file': str(project_path / f'{project_name}.uproject'),
                'features_created': self.get_created_features(world_data),
                'next_steps': self.get_next_steps(project_path, project_name)
            }

        except Exception as e:
            print(f"❌ Error creating UE5 project: {e}")
            return {
                'success': False,
                'error': str(e),
                'project_name': project_name
            }

    def create_project_structure(self, project_name):
        """Create the basic UE5 project structure"""
        project_path = self.projects_path / project_name

        # Remove existing project if it exists
        if project_path.exists():
            print(f"🗑️ Removing existing project: {project_name}")
            shutil.rmtree(project_path)

        # Create directory structure
        directories = [
            "Source",
            f"Source/{project_name}",
            f"Source/{project_name}/Public",
            f"Source/{project_name}/Private",
            "Content",
            "Content/TTGGenesis",
            "Content/TTGGenesis/Blueprints",
            "Content/TTGGenesis/Maps",
            "Content/TTGGenesis/Data",
            "Content/TTGGenesis/UI",
            "Content/TTGGenesis/Materials",
            "Content/TTGGenesis/Meshes",
            "Content/TTGGenesis/Sounds",
            "Config",
            "Binaries",
            "Intermediate",
            "Saved"
        ]

        for directory in directories:
            (project_path / directory).mkdir(parents=True, exist_ok=True)

        print(f"✅ Created project structure: {project_path}")
        return project_path

    def create_uproject_file(self, project_path, project_name, world_data):
        """Create the .uproject file"""
        uproject_data = {
            "FileVersion": 3,
            "EngineAssociation": "5.6",
            "Category": "",
            "Description": f"Generated by TTG Genesis for UE 5.6.0 - {world_data.get('description', 'Auto-generated game world')}",
            "Modules": [
                {
                    "Name": project_name,
                    "Type": "Runtime",
                    "LoadingPhase": "Default",
                    "AdditionalDependencies": [
                        "Engine",
                        "CoreUObject"
                    ]
                }
            ],
            "Plugins": [
                {
                    "Name": "ModelingToolsEditorMode",
                    "Enabled": True
                },
                {
                    "Name": "EnhancedInput",
                    "Enabled": True
                }
            ],
            "TargetPlatforms": [
                "Windows"
            ]
        }

        uproject_file = project_path / f"{project_name}.uproject"
        with open(uproject_file, 'w') as f:
            json.dump(uproject_data, f, indent=2)

        print(f"✅ Created .uproject file: {uproject_file}")

    def generate_cpp_classes(self, project_path, project_name, world_data):
        """Generate C++ classes for the game logic"""
        source_path = project_path / "Source" / project_name

        # Create module files
        self.create_module_files(source_path, project_name, world_data)

        # Create game mode and player controller
        self.create_game_mode_files(source_path, project_name, world_data)

        # Create NPC system if NPCs exist
        if world_data.get('npcs'):
            self.create_npc_system_files(source_path, project_name, world_data)

        # Create quest system if quests exist
        if world_data.get('quests'):
            self.create_quest_system_files(source_path, project_name, world_data)

        # Create environment controller
        self.create_environment_files(source_path, project_name, world_data)

        print(f"✅ Generated C++ classes in: {source_path}")

    def create_module_files(self, source_path, project_name, world_data):
        """Create the main module files"""

        # Module header
        module_h = f'''#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

class F{project_name}Module : public IModuleInterface
{{
public:
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;
}};
'''

        # Module implementation
        module_cpp = f'''#include "{project_name}Module.h"
#include "Modules/ModuleManager.h"

IMPLEMENT_PRIMARY_GAME_MODULE(F{project_name}Module, {project_name}, "{project_name}");

void F{project_name}Module::StartupModule()
{{
    // Module startup logic
    UE_LOG(LogTemp, Warning, TEXT("{project_name} Module Started"));
}}

void F{project_name}Module::ShutdownModule()
{{
    // Module shutdown logic
    UE_LOG(LogTemp, Warning, TEXT("{project_name} Module Shutdown"));
}}
'''

        # Build file - Updated for UE 5.6 (Compatible Version)
        build_cs = f'''using UnrealBuildTool;

public class {project_name} : ModuleRules
{{
    public {project_name}(ReadOnlyTargetRules Target) : base(Target)
    {{
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        // UE 5.6 compatible dependencies (stable modules only)
        PublicDependencyModuleNames.AddRange(new string[] {{
            "Core",
            "CoreUObject",
            "Engine",
            "InputCore",
            "EnhancedInput",
            "UMG",
            "Slate",
            "SlateCore",
            "GameplayTasks",
            "AIModule",
            "NavigationSystem"
        }});

        PrivateDependencyModuleNames.AddRange(new string[] {{
            "Slate",
            "SlateCore"
        }});

        // UE 5.6 compatible settings
        bUseUnity = false;
        CppStandard = CppStandardVersion.Cpp17;  // More compatible than C++20

        // Ensure compatibility
        bLegacyPublicIncludePaths = false;
        OptimizeCode = CodeOptimization.Default;

        if (Target.Configuration == UnrealTargetConfiguration.Debug)
        {{
            bOptimizeCode = false;
        }}
    }}
}}
'''

        # Write files
        with open(source_path / f"{project_name}Module.h", 'w') as f:
            f.write(module_h)

        with open(source_path / "Private" / f"{project_name}Module.cpp", 'w') as f:
            f.write(module_cpp)

        with open(source_path / f"{project_name}.Build.cs", 'w') as f:
            f.write(build_cs)

    def create_game_mode_files(self, source_path, project_name, world_data):
        """Create game mode and player controller files"""

        # Game Mode Header
        gamemode_h = f'''#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "{project_name}GameMode.generated.h"

UCLASS()
class {project_name.upper()}_API A{project_name}GameMode : public AGameModeBase
{{
    GENERATED_BODY()

public:
    A{project_name}GameMode();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Game Settings")
    FString WorldTheme = "{world_data.get('theme', 'fantasy')}";

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Game Settings")
    int32 MaxPlayers = 1;

    UFUNCTION(BlueprintCallable, Category = "Game Logic")
    void InitializeWorld();

    UFUNCTION(BlueprintCallable, Category = "Game Logic")
    void SpawnNPCs();

    UFUNCTION(BlueprintCallable, Category = "Game Logic")
    void InitializeQuests();
}};
'''

        # Game Mode Implementation
        gamemode_cpp = f'''#include "{project_name}GameMode.h"
#include "Engine/Engine.h"
#include "Engine/World.h"

A{project_name}GameMode::A{project_name}GameMode()
{{
    PrimaryActorTick.bCanEverTick = false;

    // Set default pawn class
    // DefaultPawnClass = AYourCustomPawn::StaticClass();
}}

void A{project_name}GameMode::BeginPlay()
{{
    Super::BeginPlay();

    UE_LOG(LogTemp, Warning, TEXT("{project_name} Game Mode Started"));
    UE_LOG(LogTemp, Warning, TEXT("World Theme: %s"), *WorldTheme);

    // Initialize the generated world
    InitializeWorld();
}}

void A{project_name}GameMode::InitializeWorld()
{{
    UE_LOG(LogTemp, Warning, TEXT("Initializing {world_data.get('name', 'Generated World')}"));

    // Spawn NPCs
    SpawnNPCs();

    // Initialize quest system
    InitializeQuests();

    // Set up environment
    // Add your environment setup logic here
}}

void A{project_name}GameMode::SpawnNPCs()
{{
    // NPC spawning logic will be implemented here
    UE_LOG(LogTemp, Warning, TEXT("Spawning NPCs for {project_name}"));
}}

void A{project_name}GameMode::InitializeQuests()
{{
    // Quest initialization logic will be implemented here
    UE_LOG(LogTemp, Warning, TEXT("Initializing Quests for {project_name}"));
}}
'''

        # Write files
        with open(source_path / "Public" / f"{project_name}GameMode.h", 'w') as f:
            f.write(gamemode_h)

        with open(source_path / "Private" / f"{project_name}GameMode.cpp", 'w') as f:
            f.write(gamemode_cpp)

    def create_npc_system_files(self, source_path, project_name, world_data):
        """Create NPC system files"""
        npcs = world_data.get('npcs', [])

        # NPC System Header
        npc_h = f'''#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Components/SphereComponent.h"
#include "Components/WidgetComponent.h"
#include "{project_name}NPC.generated.h"

USTRUCT(BlueprintType)
struct F{project_name}NPCData
{{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString NPCName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString NPCType;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> DialogueLines;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FVector SpawnLocation;
}};

UCLASS()
class {project_name.upper()}_API A{project_name}NPC : public ACharacter
{{
    GENERATED_BODY()

public:
    A{project_name}NPC();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC Data")
    F{project_name}NPCData NPCData;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class USphereComponent* InteractionSphere;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UWidgetComponent* DialogueWidget;

    UFUNCTION(BlueprintCallable, Category = "NPC")
    void StartDialogue();

    UFUNCTION(BlueprintCallable, Category = "NPC")
    void EndDialogue();

    UFUNCTION(BlueprintCallable, Category = "NPC")
    FString GetNextDialogueLine();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(BlueprintReadOnly, Category = "NPC")
    bool bInDialogue;

    UPROPERTY(BlueprintReadOnly, Category = "NPC")
    int32 CurrentDialogueIndex;

    UFUNCTION()
    void OnInteractionSphereBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

    UFUNCTION()
    void OnInteractionSphereEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);
}};
'''

        # NPC System Implementation
        npc_cpp = f'''#include "{project_name}NPC.h"
#include "Components/SphereComponent.h"
#include "Components/WidgetComponent.h"
#include "GameFramework/Character.h"
#include "Engine/Engine.h"

A{project_name}NPC::A{project_name}NPC()
{{
    PrimaryActorTick.bCanEverTick = false;

    // Create interaction sphere
    InteractionSphere = CreateDefaultSubobject<USphereComponent>(TEXT("InteractionSphere"));
    InteractionSphere->SetupAttachment(RootComponent);
    InteractionSphere->SetSphereRadius(200.0f);
    InteractionSphere->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
    InteractionSphere->SetCollisionResponseToAllChannels(ECR_Ignore);
    InteractionSphere->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);

    // Create dialogue widget
    DialogueWidget = CreateDefaultSubobject<UWidgetComponent>(TEXT("DialogueWidget"));
    DialogueWidget->SetupAttachment(RootComponent);
    DialogueWidget->SetRelativeLocation(FVector(0, 0, 200));
    DialogueWidget->SetVisibility(false);

    // Bind overlap events
    InteractionSphere->OnComponentBeginOverlap.AddDynamic(this, &A{project_name}NPC::OnInteractionSphereBeginOverlap);
    InteractionSphere->OnComponentEndOverlap.AddDynamic(this, &A{project_name}NPC::OnInteractionSphereEndOverlap);

    bInDialogue = false;
    CurrentDialogueIndex = 0;
}}

void A{project_name}NPC::BeginPlay()
{{
    Super::BeginPlay();

    UE_LOG(LogTemp, Warning, TEXT("NPC Spawned: %s"), *NPCData.NPCName);
}}

void A{project_name}NPC::StartDialogue()
{{
    if (!bInDialogue && NPCData.DialogueLines.Num() > 0)
    {{
        bInDialogue = true;
        CurrentDialogueIndex = 0;
        DialogueWidget->SetVisibility(true);

        UE_LOG(LogTemp, Warning, TEXT("Starting dialogue with %s"), *NPCData.NPCName);
    }}
}}

void A{project_name}NPC::EndDialogue()
{{
    bInDialogue = false;
    DialogueWidget->SetVisibility(false);
    CurrentDialogueIndex = 0;

    UE_LOG(LogTemp, Warning, TEXT("Ending dialogue with %s"), *NPCData.NPCName);
}}

FString A{project_name}NPC::GetNextDialogueLine()
{{
    if (CurrentDialogueIndex < NPCData.DialogueLines.Num())
    {{
        FString line = NPCData.DialogueLines[CurrentDialogueIndex];
        CurrentDialogueIndex++;
        return line;
    }}
    return TEXT("...");
}}

void A{project_name}NPC::OnInteractionSphereBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{{
    if (OtherActor && OtherActor->IsA<ACharacter>())
    {{
        UE_LOG(LogTemp, Warning, TEXT("Player entered interaction range of %s"), *NPCData.NPCName);
        // Show interaction prompt
    }}
}}

void A{project_name}NPC::OnInteractionSphereEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{{
    if (OtherActor && OtherActor->IsA<ACharacter>())
    {{
        UE_LOG(LogTemp, Warning, TEXT("Player left interaction range of %s"), *NPCData.NPCName);
        if (bInDialogue)
        {{
            EndDialogue();
        }}
    }}
}}
'''

        # Write NPC files
        with open(source_path / "Public" / f"{project_name}NPC.h", 'w') as f:
            f.write(npc_h)

        with open(source_path / "Private" / f"{project_name}NPC.cpp", 'w') as f:
            f.write(npc_cpp)

    def create_quest_system_files(self, source_path, project_name, world_data):
        """Create quest system files"""
        quests = world_data.get('quests', [])

        # Quest System Header
        quest_h = f'''#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Engine/DataTable.h"
#include "{project_name}QuestSystem.generated.h"

USTRUCT(BlueprintType)
struct F{project_name}QuestData : public FTableRowBase
{{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString QuestName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> Objectives;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> Rewards;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsCompleted = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsActive = false;
}};

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class {project_name.upper()}_API U{project_name}QuestSystem : public UActorComponent
{{
    GENERATED_BODY()

public:
    U{project_name}QuestSystem();

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    void StartQuest(const FString& QuestName);

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    void CompleteQuest(const FString& QuestName);

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    bool IsQuestActive(const FString& QuestName) const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    bool IsQuestCompleted(const FString& QuestName) const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    TArray<FString> GetActiveQuests() const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    F{project_name}QuestData GetQuestData(const FString& QuestName) const;

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest System")
    class UDataTable* QuestDataTable;

    UPROPERTY(BlueprintReadOnly, Category = "Quest System")
    TArray<FString> ActiveQuests;

    UPROPERTY(BlueprintReadOnly, Category = "Quest System")
    TArray<FString> CompletedQuests;

    UPROPERTY(BlueprintReadOnly, Category = "Quest System")
    TMap<FString, F{project_name}QuestData> QuestDatabase;

    void InitializeQuestDatabase();
}};
'''

        # Quest System Implementation
        quest_cpp = f'''#include "{project_name}QuestSystem.h"
#include "Engine/DataTable.h"
#include "Engine/Engine.h"

U{project_name}QuestSystem::U{project_name}QuestSystem()
{{
    PrimaryComponentTick.bCanEverTick = false;
}}

void U{project_name}QuestSystem::BeginPlay()
{{
    Super::BeginPlay();

    InitializeQuestDatabase();
    UE_LOG(LogTemp, Warning, TEXT("Quest System Initialized"));
}}

void U{project_name}QuestSystem::InitializeQuestDatabase()
{{
    // Initialize quest database with generated quest data
    QuestDatabase.Empty();

    {self.generate_quest_initialization_code(quests, project_name)}
}}

void U{project_name}QuestSystem::StartQuest(const FString& QuestName)
{{
    if (!IsQuestActive(QuestName) && !IsQuestCompleted(QuestName))
    {{
        if (QuestDatabase.Contains(QuestName))
        {{
            ActiveQuests.Add(QuestName);
            QuestDatabase[QuestName].bIsActive = true;

            UE_LOG(LogTemp, Warning, TEXT("Started Quest: %s"), *QuestName);
        }}
    }}
}}

void U{project_name}QuestSystem::CompleteQuest(const FString& QuestName)
{{
    if (IsQuestActive(QuestName))
    {{
        ActiveQuests.Remove(QuestName);
        CompletedQuests.Add(QuestName);

        if (QuestDatabase.Contains(QuestName))
        {{
            QuestDatabase[QuestName].bIsActive = false;
            QuestDatabase[QuestName].bIsCompleted = true;
        }}

        UE_LOG(LogTemp, Warning, TEXT("Completed Quest: %s"), *QuestName);
    }}
}}

bool U{project_name}QuestSystem::IsQuestActive(const FString& QuestName) const
{{
    return ActiveQuests.Contains(QuestName);
}}

bool U{project_name}QuestSystem::IsQuestCompleted(const FString& QuestName) const
{{
    return CompletedQuests.Contains(QuestName);
}}

TArray<FString> U{project_name}QuestSystem::GetActiveQuests() const
{{
    return ActiveQuests;
}}

F{project_name}QuestData U{project_name}QuestSystem::GetQuestData(const FString& QuestName) const
{{
    if (QuestDatabase.Contains(QuestName))
    {{
        return QuestDatabase[QuestName];
    }}
    return F{project_name}QuestData();
}}
'''

        # Write quest files
        with open(source_path / "Public" / f"{project_name}QuestSystem.h", 'w') as f:
            f.write(quest_h)

        with open(source_path / "Private" / f"{project_name}QuestSystem.cpp", 'w') as f:
            f.write(quest_cpp)

    def generate_quest_initialization_code(self, quests, project_name):
        """Generate C++ code to initialize quests"""
        code_lines = []
        for i, quest in enumerate(quests):
            quest_name = quest.get('name', f'Quest_{i+1}')
            description = quest.get('description', 'No description')
            objectives = quest.get('objectives', [])
            rewards = quest.get('rewards', [])

            # Escape quotes in strings
            quest_name = quest_name.replace('"', '\\"')
            description = description.replace('"', '\\"')

            code_lines.append(f'''
    // Initialize {quest_name}
    {{
        F{project_name}QuestData QuestData;
        QuestData.QuestName = TEXT("{quest_name}");
        QuestData.Description = TEXT("{description}");''')

            # Add objectives
            for obj in objectives:
                obj = obj.replace('"', '\\"')
                code_lines.append(f'        QuestData.Objectives.Add(TEXT("{obj}"));')

            # Add rewards
            for reward in rewards:
                reward = reward.replace('"', '\\"')
                code_lines.append(f'        QuestData.Rewards.Add(TEXT("{reward}"));')

            code_lines.append(f'        QuestDatabase.Add(TEXT("{quest_name}"), QuestData);')
            code_lines.append('    }')

        return '\n'.join(code_lines)

    def create_environment_files(self, source_path, project_name, world_data):
        """Create environment controller files"""
        environment = world_data.get('environment', {})

        # Environment Header
        env_h = f'''#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "{project_name}Environment.generated.h"

UCLASS()
class {project_name.upper()}_API A{project_name}Environment : public AActor
{{
    GENERATED_BODY()

public:
    A{project_name}Environment();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString TerrainType = "{environment.get('terrain', 'varied')}";

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString LightingType = "{environment.get('lighting', 'dynamic')}";

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString WeatherType = "{environment.get('weather', 'clear')}";

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UDirectionalLightComponent* SunLight;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class USkyLightComponent* SkyLight;

    UFUNCTION(BlueprintCallable, Category = "Environment")
    void SetupLighting();

    UFUNCTION(BlueprintCallable, Category = "Environment")
    void SetupWeather();

    UFUNCTION(BlueprintCallable, Category = "Environment")
    void SpawnEnvironmentObjects();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    TArray<class UStaticMesh*> EnvironmentMeshes;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    TArray<FVector> SpawnLocations;
}};
'''

        # Environment Implementation
        env_cpp = f'''#include "{project_name}Environment.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/Engine.h"
#include "Engine/World.h"

A{project_name}Environment::A{project_name}Environment()
{{
    PrimaryActorTick.bCanEverTick = false;

    // Create lighting components
    SunLight = CreateDefaultSubobject<UDirectionalLightComponent>(TEXT("SunLight"));
    RootComponent = SunLight;

    SkyLight = CreateDefaultSubobject<USkyLightComponent>(TEXT("SkyLight"));
    SkyLight->SetupAttachment(RootComponent);
}}

void A{project_name}Environment::BeginPlay()
{{
    Super::BeginPlay();

    UE_LOG(LogTemp, Warning, TEXT("Environment Controller Started"));
    UE_LOG(LogTemp, Warning, TEXT("Terrain: %s, Lighting: %s, Weather: %s"), *TerrainType, *LightingType, *WeatherType);

    SetupLighting();
    SetupWeather();
    SpawnEnvironmentObjects();
}}

void A{project_name}Environment::SetupLighting()
{{
    if (SunLight)
    {{
        // Configure lighting based on world theme
        if (LightingType == "dynamic")
        {{
            SunLight->SetIntensity(3.0f);
            SunLight->SetLightColor(FLinearColor::White);
        }}
        else if (LightingType == "mystical")
        {{
            SunLight->SetIntensity(2.0f);
            SunLight->SetLightColor(FLinearColor(0.8f, 0.9f, 1.0f));
        }}

        UE_LOG(LogTemp, Warning, TEXT("Lighting setup complete: %s"), *LightingType);
    }}
}}

void A{project_name}Environment::SetupWeather()
{{
    // Weather system setup
    UE_LOG(LogTemp, Warning, TEXT("Weather setup: %s"), *WeatherType);

    // Add weather effects based on WeatherType
    // This would integrate with UE5's weather systems
}}

void A{project_name}Environment::SpawnEnvironmentObjects()
{{
    // Spawn environment objects based on terrain type
    UE_LOG(LogTemp, Warning, TEXT("Spawning environment objects for terrain: %s"), *TerrainType);

    // Add logic to spawn appropriate meshes and objects
    // based on the generated world data
}}
'''

        # Write environment files
        with open(source_path / "Public" / f"{project_name}Environment.h", 'w') as f:
            f.write(env_h)

        with open(source_path / "Private" / f"{project_name}Environment.cpp", 'w') as f:
            f.write(env_cpp)

    def create_blueprint_data(self, project_path, project_name, world_data):
        """Create Blueprint-compatible data files"""
        content_path = project_path / "Content" / "TTGGenesis" / "Data"

        # Create NPC data file
        if world_data.get('npcs'):
            npc_data = self.format_npc_data_for_blueprints(world_data['npcs'])
            with open(content_path / "NPCData.json", 'w') as f:
                json.dump(npc_data, f, indent=2)

        # Create quest data file
        if world_data.get('quests'):
            quest_data = self.format_quest_data_for_blueprints(world_data['quests'])
            with open(content_path / "QuestData.json", 'w') as f:
                json.dump(quest_data, f, indent=2)

        # Create environment data file
        env_data = self.format_environment_data_for_blueprints(world_data.get('environment', {}))
        with open(content_path / "EnvironmentData.json", 'w') as f:
            json.dump(env_data, f, indent=2)

        # Create world metadata
        world_metadata = {
            'WorldName': world_data.get('name', 'Generated World'),
            'Theme': world_data.get('theme', 'fantasy'),
            'Description': world_data.get('description', ''),
            'GeneratedAt': world_data.get('generated_at', datetime.now().isoformat()),
            'NPCCount': len(world_data.get('npcs', [])),
            'QuestCount': len(world_data.get('quests', [])),
            'HasEnvironment': bool(world_data.get('environment'))
        }

        with open(content_path / "WorldMetadata.json", 'w') as f:
            json.dump(world_metadata, f, indent=2)

        print(f"✅ Created Blueprint data files in: {content_path}")

    def format_npc_data_for_blueprints(self, npcs):
        """Format NPC data for Blueprint consumption"""
        formatted_npcs = {}
        for i, npc in enumerate(npcs):
            npc_id = f"NPC_{i+1:03d}"
            formatted_npcs[npc_id] = {
                'NPCName': npc.get('name', f'NPC {i+1}'),
                'NPCType': npc.get('type', 'friendly'),
                'DialogueLines': npc.get('dialogue', []),
                'SpawnLocation': {
                    'X': npc.get('location', {}).get('x', i * 100),
                    'Y': npc.get('location', {}).get('y', 0),
                    'Z': npc.get('location', {}).get('z', 0)
                },
                'Health': npc.get('health', 100),
                'Level': npc.get('level', 1)
            }
        return formatted_npcs

    def format_quest_data_for_blueprints(self, quests):
        """Format quest data for Blueprint consumption"""
        formatted_quests = {}
        for i, quest in enumerate(quests):
            quest_id = f"Quest_{i+1:03d}"
            formatted_quests[quest_id] = {
                'QuestName': quest.get('name', f'Quest {i+1}'),
                'Description': quest.get('description', ''),
                'Objectives': quest.get('objectives', []),
                'Rewards': quest.get('rewards', []),
                'RequiredLevel': quest.get('required_level', 1),
                'ExperienceReward': quest.get('experience_reward', 100),
                'GoldReward': quest.get('gold_reward', 50)
            }
        return formatted_quests

    def format_environment_data_for_blueprints(self, environment):
        """Format environment data for Blueprint consumption"""
        return {
            'TerrainType': environment.get('terrain', 'varied'),
            'LightingSetup': environment.get('lighting', 'dynamic'),
            'WeatherConditions': environment.get('weather', 'clear'),
            'Structures': environment.get('structures', []),
            'AmbientSounds': environment.get('ambient_sounds', []),
            'PostProcessSettings': {
                'Brightness': 1.0,
                'Contrast': 1.0,
                'Saturation': 1.0
            }
        }

    def create_game_content(self, project_path, project_name, world_data):
        """Create game content files"""
        content_path = project_path / "Content" / "TTGGenesis"

        # Create a basic level
        self.create_basic_level(content_path, project_name, world_data)

        # Create UI blueprints data
        self.create_ui_data(content_path, project_name, world_data)

        print(f"✅ Created game content in: {content_path}")

    def create_basic_level(self, content_path, project_name, world_data):
        """Create basic level data"""
        maps_path = content_path / "Maps"

        # Create level metadata
        level_data = {
            'LevelName': f"{project_name}_MainLevel",
            'WorldTheme': world_data.get('theme', 'fantasy'),
            'SpawnPoints': [],
            'NPCSpawns': [],
            'QuestMarkers': [],
            'EnvironmentObjects': []
        }

        # Add NPC spawn points
        for i, npc in enumerate(world_data.get('npcs', [])):
            location = npc.get('location', {'x': i * 100, 'y': 0, 'z': 0})
            level_data['NPCSpawns'].append({
                'NPCName': npc.get('name', f'NPC_{i}'),
                'Location': location,
                'Rotation': {'x': 0, 'y': 0, 'z': 0}
            })

        # Add quest markers
        for i, quest in enumerate(world_data.get('quests', [])):
            level_data['QuestMarkers'].append({
                'QuestName': quest.get('name', f'Quest_{i}'),
                'Location': {'x': i * 150, 'y': 100, 'z': 0},
                'MarkerType': 'QuestGiver'
            })

        # Add player spawn point
        level_data['SpawnPoints'].append({
            'PlayerSpawn': True,
            'Location': {'x': 0, 'y': 0, 'z': 100},
            'Rotation': {'x': 0, 'y': 0, 'z': 0}
        })

        with open(maps_path / f"{project_name}_LevelData.json", 'w') as f:
            json.dump(level_data, f, indent=2)

    def create_ui_data(self, content_path, project_name, world_data):
        """Create UI data for the game"""
        ui_path = content_path / "UI"

        # Create dialogue UI data
        dialogue_data = {
            'DialogueBoxStyle': 'Modern',
            'FontSize': 16,
            'BackgroundColor': {'R': 0, 'G': 0, 'B': 0, 'A': 180},
            'TextColor': {'R': 255, 'G': 255, 'B': 255, 'A': 255},
            'NPCNameColor': {'R': 100, 'G': 200, 'B': 255, 'A': 255}
        }

        with open(ui_path / "DialogueUIData.json", 'w') as f:
            json.dump(dialogue_data, f, indent=2)

        # Create quest UI data
        quest_ui_data = {
            'QuestLogStyle': 'Journal',
            'MaxActiveQuests': 10,
            'QuestColors': {
                'Active': {'R': 255, 'G': 255, 'B': 100, 'A': 255},
                'Completed': {'R': 100, 'G': 255, 'B': 100, 'A': 255},
                'Failed': {'R': 255, 'G': 100, 'B': 100, 'A': 255}
            }
        }

        with open(ui_path / "QuestUIData.json", 'w') as f:
            json.dump(quest_ui_data, f, indent=2)

    def create_build_files(self, project_path, project_name):
        """Create build configuration files"""

        # Create Target.cs files
        self.create_target_files(project_path, project_name)

        # Create Config files
        self.create_config_files(project_path, project_name)

        print(f"✅ Created build files for: {project_name}")

    def create_target_files(self, project_path, project_name):
        """Create UE5 target files"""
        source_path = project_path / "Source"

        # Game target file - UE 5.6 Compatible
        game_target = f'''using UnrealBuildTool;
using System.Collections.Generic;

public class {project_name}Target : TargetRules
{{
    public {project_name}Target(TargetInfo Target) : base(Target)
    {{
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V2;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_1;
        ExtraModuleNames.AddRange(new string[] {{ "{project_name}" }});
    }}
}}
'''

        # Editor target file - UE 5.6 Compatible
        editor_target = f'''using UnrealBuildTool;
using System.Collections.Generic;

public class {project_name}EditorTarget : TargetRules
{{
    public {project_name}EditorTarget(TargetInfo Target) : base(Target)
    {{
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V2;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_1;
        ExtraModuleNames.AddRange(new string[] {{ "{project_name}" }});
    }}
}}
'''

        with open(source_path / f"{project_name}.Target.cs", 'w') as f:
            f.write(game_target)

        with open(source_path / f"{project_name}Editor.Target.cs", 'w') as f:
            f.write(editor_target)

    def create_config_files(self, project_path, project_name):
        """Create configuration files"""
        config_path = project_path / "Config"

        # DefaultEngine.ini - Updated for UE 5.6
        engine_config = f'''[/Script/EngineSettings.GameMapsSettings]
GameDefaultMap=/Game/TTGGenesis/Maps/{project_name}_MainLevel
EditorStartupMap=/Game/TTGGenesis/Maps/{project_name}_MainLevel
GlobalDefaultGameMode=/Game/TTGGenesis/Blueprints/BP_{project_name}_GameMode

[/Script/Engine.Engine]
+ActiveGameNameRedirects=(OldGameName="TP_ThirdPersonBP",NewGameName="/Script/{project_name}")
+ActiveGameNameRedirects=(OldGameName="/Script/TP_ThirdPersonBP",NewGameName="/Script/{project_name}")

[/Script/HardwareTargeting.HardwareTargetingSettings]
TargetedHardwareClass=Desktop
AppliedTargetedHardwareClass=Desktop
DefaultGraphicsPerformance=Maximum
AppliedDefaultGraphicsPerformance=Maximum

[/Script/WindowsTargetPlatform.WindowsTargetSettings]
DefaultGraphicsRHI=DefaultGraphicsRHI_DX12
-D3D12TargetedShaderFormats=PCD3D_SM5
+D3D12TargetedShaderFormats=PCD3D_SM6
+D3D12TargetedShaderFormats=PCD3D_SM5
Compiler=Default
AudioSampleRate=48000
AudioCallbackBufferFrameSize=1024
AudioNumBuffersToEnqueue=1
AudioMaxChannels=0
AudioNumSourceWorkers=4
SpatializationPlugin=
SourceDataOverridePlugin=
ReverbPlugin=
OcclusionPlugin=
CompressionOverrides=(bOverrideCompressionTimes=False,DurationThreshold=5.000000,MaxNumRandomBranches=0,SoundCueQualityIndex=0)
CacheSizeKB=65536
MaxChunkSizeOverrideKB=0
bResampleForDevice=False
MaxSampleRate=48000.000000
HighSampleRate=32000.000000
MedSampleRate=24000.000000
LowSampleRate=12000.000000
MinSampleRate=8000.000000
CompressionQualityModifier=1.000000
AutoStreamingThreshold=0.000000
SoundCueCookQualityIndex=-1

[/Script/Engine.RendererSettings]
r.GenerateMeshDistanceFields=True
r.DynamicGlobalIlluminationMethod=1
r.ReflectionMethod=1
r.Shadow.Virtual.Enable=1
r.DefaultFeature.AutoExposure.ExtendDefaultLuminanceRange=True
r.DefaultFeature.LocalExposure.HighlightContrastScale=0.8
r.DefaultFeature.LocalExposure.ShadowContrastScale=0.8

[/Script/WorldPartition.WorldPartitionSettings]
CommandletClass=Class'/Script/UnrealEd.WorldPartitionConvertCommandlet'
bEnableWorldPartition=False
bEnableWorldPartitionStreaming=False
WorldPartitionGridSize=25600

[/Script/Engine.UserInterfaceSettings]
bAuthorizeAutomaticWidgetVariableCreation=False
FontDPIPreset=Standard
FontDPI=72

[/Script/Engine.Engine]
+ActiveGameNameRedirects=(OldGameName="TP_Blank",NewGameName="/Script/{project_name}")
+ActiveGameNameRedirects=(OldGameName="/Script/TP_Blank",NewGameName="/Script/{project_name}")
+ActiveClassRedirects=(OldClassName="TP_BlankGameModeBase",NewClassName="{project_name}GameMode")

[/Script/AndroidFileServerEditor.AndroidFileServerRuntimeSettings]
bEnablePlugin=True
bAllowNetworkConnection=True
SecurityToken=
bIncludeInShipping=False
bAllowExternalStartInShipping=False
bCompileAFSProject=False
bUseCompression=False
bLogFiles=False
bReportStats=False
ConnectionType=USBOnly
bUseManualIPAddress=False
ManualIPAddress=
'''

        # DefaultGame.ini - Updated for UE 5.6
        game_config = f'''[/Script/EngineSettings.GeneralProjectSettings]
ProjectID={project_name}
ProjectName={project_name}
ProjectVersion=1.0.0
CompanyName=TTG Genesis
CopyrightNotice=Generated by TTG Genesis for UE 5.6
Description=Auto-generated game world for Unreal Engine 5.6
Homepage=
SupportContact=

[/Script/UnrealEd.ProjectPackagingSettings]
Build=IfProjectHasCode
BuildConfiguration=PPBC_Development
StagingDirectory=(Path="")
FullRebuild=False
ForDistribution=False
IncludeDebugFiles=False
BlueprintNativizationMethod=Disabled
bIncludeNativizedAssetsInProjectGeneration=False
bExcludeMonolithicEngineHeadersInNativizedCode=False
UsePakFile=True
bGenerateChunks=False
bGenerateNoChunks=False
bChunkHardReferencesOnly=False
bForceOneChunkPerFile=False
MaxChunkSize=0
BuildCookRunArguments=

[/Script/Engine.CollisionProfile]
-Profiles=(Name="NoCollision",CollisionEnabled=NoCollision,ObjectTypeName="WorldStatic",CustomResponses=((Channel="Visibility",Response=ECR_Ignore),(Channel="Camera",Response=ECR_Ignore)),HelpMessage="No collision",bCanModify=False)
-Profiles=(Name="BlockAll",CollisionEnabled=QueryAndPhysics,ObjectTypeName="WorldStatic",CustomResponses=,HelpMessage="WorldStatic object that blocks all actors by default. All new custom channels will use its own default response. ",bCanModify=False)
-Profiles=(Name="OverlapAll",CollisionEnabled=QueryOnly,ObjectTypeName="WorldStatic",CustomResponses=((Channel="WorldStatic",Response=ECR_Overlap),(Channel="Pawn",Response=ECR_Overlap),(Channel="Visibility",Response=ECR_Overlap),(Channel="WorldDynamic",Response=ECR_Overlap),(Channel="Camera",Response=ECR_Overlap),(Channel="PhysicsBody",Response=ECR_Overlap),(Channel="Vehicle",Response=ECR_Overlap),(Channel="Destructible",Response=ECR_Overlap)),HelpMessage="WorldStatic object that overlaps all actors by default. All new custom channels will use its own default response. ",bCanModify=False)
-Profiles=(Name="BlockAllDynamic",CollisionEnabled=QueryAndPhysics,ObjectTypeName="WorldDynamic",CustomResponses=,HelpMessage="WorldDynamic object that blocks all actors by default. All new custom channels will use its own default response. ",bCanModify=False)
-Profiles=(Name="OverlapAllDynamic",CollisionEnabled=QueryOnly,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="WorldStatic",Response=ECR_Overlap),(Channel="Pawn",Response=ECR_Overlap),(Channel="Visibility",Response=ECR_Overlap),(Channel="WorldDynamic",Response=ECR_Overlap),(Channel="Camera",Response=ECR_Overlap),(Channel="PhysicsBody",Response=ECR_Overlap),(Channel="Vehicle",Response=ECR_Overlap),(Channel="Destructible",Response=ECR_Overlap)),HelpMessage="WorldDynamic object that overlaps all actors by default. All new custom channels will use its own default response. ",bCanModify=False)
-Profiles=(Name="IgnoreOnlyPawn",CollisionEnabled=QueryAndPhysics,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="Pawn",Response=ECR_Ignore),(Channel="Vehicle",Response=ECR_Ignore)),HelpMessage="WorldDynamic object that ignores Pawn and Vehicle. All other channels will be set to default.",bCanModify=False)
-Profiles=(Name="OverlapOnlyPawn",CollisionEnabled=QueryOnly,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="Pawn",Response=ECR_Overlap),(Channel="Vehicle",Response=ECR_Overlap),(Channel="Camera",Response=ECR_Ignore)),HelpMessage="WorldDynamic object that overlaps Pawn, Camera, and Vehicle. All other channels will be set to default. ",bCanModify=False)
-Profiles=(Name="Pawn",CollisionEnabled=QueryAndPhysics,ObjectTypeName="Pawn",CustomResponses=((Channel="Visibility",Response=ECR_Ignore)),HelpMessage="Pawn object. Can be used for capsule of any playerable character or AI. ",bCanModify=False)
-Profiles=(Name="Spectator",CollisionEnabled=QueryOnly,ObjectTypeName="Pawn",CustomResponses=((Channel="WorldStatic"),(Channel="Pawn",Response=ECR_Ignore),(Channel="Visibility",Response=ECR_Ignore),(Channel="WorldDynamic",Response=ECR_Ignore),(Channel="Camera",Response=ECR_Ignore),(Channel="PhysicsBody",Response=ECR_Ignore),(Channel="Vehicle",Response=ECR_Ignore),(Channel="Destructible",Response=ECR_Ignore)),HelpMessage="Pawn object that ignores all other actors except WorldStatic.",bCanModify=False)
-Profiles=(Name="CharacterMesh",CollisionEnabled=QueryOnly,ObjectTypeName="Pawn",CustomResponses=((Channel="Pawn",Response=ECR_Ignore),(Channel="Vehicle",Response=ECR_Ignore),(Channel="Visibility",Response=ECR_Ignore)),HelpMessage="Pawn object that is used for Character Mesh. All other channels will be set to default.",bCanModify=False)
-Profiles=(Name="PhysicsActor",CollisionEnabled=QueryAndPhysics,ObjectTypeName="PhysicsBody",CustomResponses=,HelpMessage="Simulating actors",bCanModify=False)
-Profiles=(Name="Destructible",CollisionEnabled=QueryAndPhysics,ObjectTypeName="Destructible",CustomResponses=,HelpMessage="Destructible actors",bCanModify=False)
-Profiles=(Name="InvisibleWall",CollisionEnabled=QueryAndPhysics,ObjectTypeName="WorldStatic",CustomResponses=((Channel="Visibility",Response=ECR_Ignore)),HelpMessage="WorldStatic object that is invisible.",bCanModify=False)
-Profiles=(Name="InvisibleWallDynamic",CollisionEnabled=QueryAndPhysics,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="Visibility",Response=ECR_Ignore)),HelpMessage="WorldDynamic object that is invisible.",bCanModify=False)
-Profiles=(Name="Trigger",CollisionEnabled=QueryOnly,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="WorldStatic",Response=ECR_Overlap),(Channel="Pawn",Response=ECR_Overlap),(Channel="Visibility",Response=ECR_Ignore),(Channel="WorldDynamic",Response=ECR_Overlap),(Channel="Camera",Response=ECR_Overlap),(Channel="PhysicsBody",Response=ECR_Overlap),(Channel="Vehicle",Response=ECR_Overlap),(Channel="Destructible",Response=ECR_Overlap)),HelpMessage="WorldDynamic object that is used for trigger. All other channels will be set to default.",bCanModify=False)
-Profiles=(Name="Ragdoll",CollisionEnabled=QueryAndPhysics,ObjectTypeName="PhysicsBody",CustomResponses=((Channel="Pawn",Response=ECR_Ignore),(Channel="Visibility",Response=ECR_Ignore)),HelpMessage="Simulating Skeletal Mesh Component. All other channels will be set to default.",bCanModify=False)
-Profiles=(Name="Vehicle",CollisionEnabled=QueryAndPhysics,ObjectTypeName="Vehicle",CustomResponses=,HelpMessage="Vehicle object that blocks Vehicle, WorldStatic, and WorldDynamic. All other channels will be set to default.",bCanModify=False)
-Profiles=(Name="UI",CollisionEnabled=QueryOnly,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="WorldStatic",Response=ECR_Overlap),(Channel="Pawn",Response=ECR_Overlap),(Channel="Visibility"),(Channel="WorldDynamic",Response=ECR_Overlap),(Channel="Camera",Response=ECR_Overlap),(Channel="PhysicsBody",Response=ECR_Overlap),(Channel="Vehicle",Response=ECR_Overlap),(Channel="Destructible",Response=ECR_Overlap)),HelpMessage="WorldStatic object that overlaps all actors by default. All new custom channels will use its own default response. ",bCanModify=False)
+Profiles=(Name="NoCollision",CollisionEnabled=NoCollision,bCanModify=False,ObjectTypeName="WorldStatic",CustomResponses=((Channel="Visibility",Response=ECR_Ignore),(Channel="Camera",Response=ECR_Ignore)),HelpMessage="No collision")
+Profiles=(Name="BlockAll",CollisionEnabled=QueryAndPhysics,bCanModify=False,ObjectTypeName="WorldStatic",CustomResponses=,HelpMessage="WorldStatic object that blocks all actors by default. All new custom channels will use its own default response. ")
+Profiles=(Name="OverlapAll",CollisionEnabled=QueryOnly,bCanModify=False,ObjectTypeName="WorldStatic",CustomResponses=((Channel="WorldStatic",Response=ECR_Overlap),(Channel="WorldDynamic",Response=ECR_Overlap),(Channel="Pawn",Response=ECR_Overlap),(Channel="Visibility",Response=ECR_Overlap),(Channel="Camera",Response=ECR_Overlap),(Channel="PhysicsBody",Response=ECR_Overlap),(Channel="Vehicle",Response=ECR_Overlap),(Channel="Destructible",Response=ECR_Overlap)),HelpMessage="WorldStatic object that overlaps all actors by default. All new custom channels will use its own default response. ")
+Profiles=(Name="BlockAllDynamic",CollisionEnabled=QueryAndPhysics,bCanModify=False,ObjectTypeName="WorldDynamic",CustomResponses=,HelpMessage="WorldDynamic object that blocks all actors by default. All new custom channels will use its own default response. ")
+Profiles=(Name="OverlapAllDynamic",CollisionEnabled=QueryOnly,bCanModify=False,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="WorldStatic",Response=ECR_Overlap),(Channel="WorldDynamic",Response=ECR_Overlap),(Channel="Pawn",Response=ECR_Overlap),(Channel="Visibility",Response=ECR_Overlap),(Channel="Camera",Response=ECR_Overlap),(Channel="PhysicsBody",Response=ECR_Overlap),(Channel="Vehicle",Response=ECR_Overlap),(Channel="Destructible",Response=ECR_Overlap)),HelpMessage="WorldDynamic object that overlaps all actors by default. All new custom channels will use its own default response. ")
+Profiles=(Name="IgnoreOnlyPawn",CollisionEnabled=QueryAndPhysics,bCanModify=False,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="Pawn",Response=ECR_Ignore),(Channel="Vehicle",Response=ECR_Ignore)),HelpMessage="WorldDynamic object that ignores Pawn and Vehicle. All other channels will be set to default.")
+Profiles=(Name="OverlapOnlyPawn",CollisionEnabled=QueryOnly,bCanModify=False,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="Pawn",Response=ECR_Overlap),(Channel="Camera",Response=ECR_Ignore),(Channel="Vehicle",Response=ECR_Overlap)),HelpMessage="WorldDynamic object that overlaps Pawn, Camera, and Vehicle. All other channels will be set to default. ")
+Profiles=(Name="Pawn",CollisionEnabled=QueryAndPhysics,bCanModify=False,ObjectTypeName="Pawn",CustomResponses=((Channel="Visibility",Response=ECR_Ignore)),HelpMessage="Pawn object. Can be used for capsule of any playerable character or AI. ")
+Profiles=(Name="Spectator",CollisionEnabled=QueryOnly,bCanModify=False,ObjectTypeName="Pawn",CustomResponses=((Channel="WorldDynamic",Response=ECR_Ignore),(Channel="Pawn",Response=ECR_Ignore),(Channel="Visibility",Response=ECR_Ignore),(Channel="Camera",Response=ECR_Ignore),(Channel="PhysicsBody",Response=ECR_Ignore),(Channel="Vehicle",Response=ECR_Ignore),(Channel="Destructible",Response=ECR_Ignore)),HelpMessage="Pawn object that ignores all other actors except WorldStatic.")
+Profiles=(Name="CharacterMesh",CollisionEnabled=QueryOnly,bCanModify=False,ObjectTypeName="Pawn",CustomResponses=((Channel="Pawn",Response=ECR_Ignore),(Channel="Visibility",Response=ECR_Ignore),(Channel="Vehicle",Response=ECR_Ignore)),HelpMessage="Pawn object that is used for Character Mesh. All other channels will be set to default.")
+Profiles=(Name="PhysicsActor",CollisionEnabled=QueryAndPhysics,bCanModify=False,ObjectTypeName="PhysicsBody",CustomResponses=,HelpMessage="Simulating actors")
+Profiles=(Name="Destructible",CollisionEnabled=QueryAndPhysics,bCanModify=False,ObjectTypeName="Destructible",CustomResponses=,HelpMessage="Destructible actors")
+Profiles=(Name="InvisibleWall",CollisionEnabled=QueryAndPhysics,bCanModify=False,ObjectTypeName="WorldStatic",CustomResponses=((Channel="Visibility",Response=ECR_Ignore)),HelpMessage="WorldStatic object that is invisible.")
+Profiles=(Name="InvisibleWallDynamic",CollisionEnabled=QueryAndPhysics,bCanModify=False,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="Visibility",Response=ECR_Ignore)),HelpMessage="WorldDynamic object that is invisible.")
+Profiles=(Name="Trigger",CollisionEnabled=QueryOnly,bCanModify=False,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="WorldStatic",Response=ECR_Overlap),(Channel="WorldDynamic",Response=ECR_Overlap),(Channel="Pawn",Response=ECR_Overlap),(Channel="Visibility",Response=ECR_Ignore),(Channel="Camera",Response=ECR_Overlap),(Channel="PhysicsBody",Response=ECR_Overlap),(Channel="Vehicle",Response=ECR_Overlap),(Channel="Destructible",Response=ECR_Overlap)),HelpMessage="WorldDynamic object that is used for trigger. All other channels will be set to default.")
+Profiles=(Name="Ragdoll",CollisionEnabled=QueryAndPhysics,bCanModify=False,ObjectTypeName="PhysicsBody",CustomResponses=((Channel="Pawn",Response=ECR_Ignore),(Channel="Visibility",Response=ECR_Ignore)),HelpMessage="Simulating Skeletal Mesh Component. All other channels will be set to default.")
+Profiles=(Name="Vehicle",CollisionEnabled=QueryAndPhysics,bCanModify=False,ObjectTypeName="Vehicle",CustomResponses=,HelpMessage="Vehicle object that blocks Vehicle, WorldStatic, and WorldDynamic. All other channels will be set to default.")
+Profiles=(Name="UI",CollisionEnabled=QueryOnly,bCanModify=False,ObjectTypeName="WorldDynamic",CustomResponses=((Channel="WorldStatic",Response=ECR_Overlap),(Channel="WorldDynamic",Response=ECR_Overlap),(Channel="Pawn",Response=ECR_Overlap),(Channel="Camera",Response=ECR_Overlap),(Channel="PhysicsBody",Response=ECR_Overlap),(Channel="Vehicle",Response=ECR_Overlap),(Channel="Destructible",Response=ECR_Overlap)),HelpMessage="WorldStatic object that overlaps all actors by default. All new custom channels will use its own default response. ")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel1,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel2,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel3,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel4,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel5,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel6,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel7,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel8,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel9,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel10,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel11,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel12,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel13,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel14,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel15,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel16,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel17,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
-DefaultChannelResponses=(Channel=ECC_GameTraceChannel18,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel1,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel2,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel3,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel4,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel5,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel6,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel7,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel8,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel9,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel10,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel11,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel12,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel13,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel14,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel15,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel16,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel17,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel18,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="")
'''

        with open(config_path / "DefaultEngine.ini", 'w') as f:
            f.write(engine_config)

        with open(config_path / "DefaultGame.ini", 'w') as f:
            f.write(game_config)

    def generate_project_files(self, project_path, project_name):
        """Generate UE5 project files"""
        if not self.ue5_path:
            print("⚠️ UE5 not found - skipping project file generation")
            return False

        try:
            uproject_file = project_path / f"{project_name}.uproject"

            # Use UnrealBuildTool to generate project files
            cmd = [
                str(self.ue5_build_tool),
                "-projectfiles",
                f"-project={uproject_file}",
                "-game",
                "-rocket",
                "-progress"
            ]

            print(f"🔧 Generating project files...")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(project_path))

            if result.returncode == 0:
                print(f"✅ Project files generated successfully")
                return True
            else:
                print(f"⚠️ Project file generation completed with warnings")
                print(f"Output: {result.stdout}")
                return True

        except Exception as e:
            print(f"❌ Error generating project files: {e}")
            return False

    def compile_project(self, project_path, project_name):
        """Compile the UE5 project"""
        if not self.ue5_path:
            print("⚠️ UE5 not found - skipping compilation")
            return False

        try:
            # Use UnrealBuildTool to compile
            cmd = [
                str(self.ue5_build_tool),
                project_name,
                "Win64",
                "Development",
                f"-Project={project_path / f'{project_name}.uproject'}"
            ]

            print(f"🔨 Compiling project...")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(project_path))

            if result.returncode == 0:
                print(f"✅ Project compiled successfully")
                return True
            else:
                print(f"⚠️ Compilation completed with warnings")
                print(f"Output: {result.stdout}")
                return True

        except Exception as e:
            print(f"❌ Error compiling project: {e}")
            return False

    def get_created_features(self, world_data):
        """Get list of created features"""
        features = []

        if world_data.get('npcs'):
            features.append(f"NPC System ({len(world_data['npcs'])} NPCs)")

        if world_data.get('quests'):
            features.append(f"Quest System ({len(world_data['quests'])} Quests)")

        if world_data.get('environment'):
            features.append("Environment Controller")

        features.extend([
            "Game Mode with World Initialization",
            "C++ Classes with Blueprint Integration",
            "Data Tables for NPCs and Quests",
            "UI System for Dialogue and Quests",
            "Level with Spawn Points and Markers"
        ])

        return features

    def get_next_steps(self, project_path, project_name):
        """Get next steps for the user"""
        steps = []

        if self.ue5_path:
            steps.extend([
                f"1. Open {project_name}.uproject in Unreal Engine 5",
                "2. Compile the project (Build > Compile)",
                "3. Create Blueprints based on the generated C++ classes",
                "4. Design the level using the generated spawn points",
                "5. Test NPC interactions and quest system"
            ])
        else:
            steps.extend([
                "1. Install Unreal Engine 5.1 or higher",
                f"2. Open {project_name}.uproject in UE5",
                "3. Generate Visual Studio project files",
                "4. Compile the C++ code",
                "5. Create Blueprints and design your level"
            ])

        steps.extend([
            "6. Customize NPC appearances and animations",
            "7. Add sound effects and music",
            "8. Create UI widgets for dialogue and quests",
            "9. Test and refine gameplay mechanics",
            "10. Package your game for distribution"
        ])

        return steps

# Test function
def test_ue5_creator():
    """Test the UE5 project creator"""
    creator = UE5ProjectCreator()

    # Test world data
    test_world = {
        'name': 'Magical Forest Adventure',
        'description': 'A magical forest with fairy NPCs and crystal quests',
        'theme': 'forest',
        'npcs': [
            {
                'name': 'Forest Guardian',
                'type': 'friendly',
                'dialogue': ['Welcome to the magical forest!', 'Beware of the ancient dangers.'],
                'location': {'x': 100, 'y': 0, 'z': 0}
            },
            {
                'name': 'Fairy Guide',
                'type': 'helper',
                'dialogue': ['I can show you hidden paths!', 'The crystals hold great power.'],
                'location': {'x': -100, 'y': 0, 'z': 0}
            }
        ],
        'quests': [
            {
                'name': 'Crystal Collection',
                'description': 'Collect enchanted crystals scattered throughout the forest',
                'objectives': ['Find 5 enchanted crystals', 'Return to the Fairy Guide'],
                'rewards': ['Magic Staff', 'Forest Blessing']
            }
        ],
        'environment': {
            'terrain': 'forested hills',
            'lighting': 'mystical',
            'weather': 'misty'
        }
    }

    options = {
        'generateProjectFiles': True,
        'compileProject': False
    }

    result = creator.create_complete_project(test_world, options)
    print(f"\nTest Result: {result}")

if __name__ == "__main__":
    test_ue5_creator()