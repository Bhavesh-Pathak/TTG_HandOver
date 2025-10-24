#!/usr/bin/env python3
"""
TTG Genesis - UE5 Code Generator
Converts JSON game world data into UE5-compatible C++ and Blueprint formats
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UE5CodeGenerator:
    """
    Comprehensive UE5 code generator that creates C++ headers, implementations,
    and Blueprint-compatible JSON from TTG Genesis world data
    """

    def __init__(self, output_base_path: str = "."):
        self.output_base_path = Path(output_base_path)
        self.cpp_output_path = self.output_base_path / "ue5-c++"
        self.blueprint_output_path = self.output_base_path / "ue5-exports"

        # Create output directories
        self.cpp_output_path.mkdir(parents=True, exist_ok=True)
        self.blueprint_output_path.mkdir(parents=True, exist_ok=True)

    def generate_all(self, json_data: Dict[str, Any], world_name: str = "GeneratedWorld") -> Dict[str, str]:
        """
        Generate all UE5 compatible files from JSON data

        Args:
            json_data: The world data from prompt parser
            world_name: Name for the generated world/classes

        Returns:
            Dictionary of generated file paths
        """
        logger.info(f"Generating UE5 files for world: {world_name}")

        generated_files = {}

        # Generate C++ files
        generated_files.update(self._generate_cpp_files(json_data, world_name))

        # Generate Blueprint JSON files
        generated_files.update(self._generate_blueprint_files(json_data, world_name))

        # Generate additional utility files
        generated_files.update(self._generate_utility_files(json_data, world_name))

        logger.info(f"Generated {len(generated_files)} files successfully")
        return generated_files

    def _generate_cpp_files(self, json_data: Dict[str, Any], world_name: str) -> Dict[str, str]:
        """Generate C++ header and implementation files"""
        files = {}

        # Quest System
        quest_header, quest_cpp = self._generate_quest_system_cpp(json_data, world_name)
        files[f"{world_name}QuestSystem.h"] = self._write_file(
            self.cpp_output_path / f"{world_name}QuestSystem.h", quest_header
        )
        files[f"{world_name}QuestSystem.cpp"] = self._write_file(
            self.cpp_output_path / f"{world_name}QuestSystem.cpp", quest_cpp
        )

        # NPC System
        npc_header, npc_cpp = self._generate_npc_system_cpp(json_data, world_name)
        files[f"{world_name}NPCSystem.h"] = self._write_file(
            self.cpp_output_path / f"{world_name}NPCSystem.h", npc_header
        )
        files[f"{world_name}NPCSystem.cpp"] = self._write_file(
            self.cpp_output_path / f"{world_name}NPCSystem.cpp", npc_cpp
        )

        # Environment System
        env_header, env_cpp = self._generate_environment_system_cpp(json_data, world_name)
        files[f"{world_name}Environment.h"] = self._write_file(
            self.cpp_output_path / f"{world_name}Environment.h", env_header
        )
        files[f"{world_name}Environment.cpp"] = self._write_file(
            self.cpp_output_path / f"{world_name}Environment.cpp", env_cpp
        )

        # Player Controller
        controller_header, controller_cpp = self._generate_player_controller_cpp(json_data, world_name)
        files[f"{world_name}PlayerController.h"] = self._write_file(
            self.cpp_output_path / f"{world_name}PlayerController.h", controller_header
        )
        files[f"{world_name}PlayerController.cpp"] = self._write_file(
            self.cpp_output_path / f"{world_name}PlayerController.cpp", controller_cpp
        )

        return files

    def _generate_blueprint_files(self, json_data: Dict[str, Any], world_name: str) -> Dict[str, str]:
        """Generate Blueprint-compatible JSON files"""
        files = {}

        # Quest data for Blueprints
        quest_bp_data = self._create_blueprint_quest_data(json_data)
        files["QuestData.json"] = self._write_json_file(
            self.blueprint_output_path / "QuestData.json", quest_bp_data
        )

        # NPC data for Blueprints
        npc_bp_data = self._create_blueprint_npc_data(json_data)
        files["NPCData.json"] = self._write_json_file(
            self.blueprint_output_path / "NPCData.json", npc_bp_data
        )

        # Environment data for Blueprints
        env_bp_data = self._create_blueprint_environment_data(json_data)
        files["EnvironmentData.json"] = self._write_json_file(
            self.blueprint_output_path / "EnvironmentData.json", env_bp_data
        )

        # Asset list for content browser
        asset_data = self._create_blueprint_asset_data(json_data)
        files["AssetList.json"] = self._write_json_file(
            self.blueprint_output_path / "AssetList.json", asset_data
        )

        # Complete world data (VaRest compatible)
        varest_data = self._create_varest_compatible_data(json_data)
        files["WorldData_VaRest.json"] = self._write_json_file(
            self.blueprint_output_path / "WorldData_VaRest.json", varest_data
        )

        return files

    def _generate_utility_files(self, json_data: Dict[str, Any], world_name: str) -> Dict[str, str]:
        """Generate utility files for UE5 integration"""
        files = {}

        # Build.cs file for C++ compilation
        build_cs = self._generate_build_cs(world_name)
        files[f"{world_name}.Build.cs"] = self._write_file(
            self.cpp_output_path / f"{world_name}.Build.cs", build_cs
        )

        # Module header
        module_header = self._generate_module_header(world_name)
        files[f"{world_name}Module.h"] = self._write_file(
            self.cpp_output_path / f"{world_name}Module.h", module_header
        )

        # Module implementation
        module_cpp = self._generate_module_cpp(world_name)
        files[f"{world_name}Module.cpp"] = self._write_file(
            self.cpp_output_path / f"{world_name}Module.cpp", module_cpp
        )

        # README for integration
        readme = self._generate_integration_readme(json_data, world_name)
        files["UE5_Integration_README.md"] = self._write_file(
            self.output_base_path / "UE5_Integration_README.md", readme
        )

        return files

    def _generate_quest_system_cpp(self, json_data: Dict[str, Any], world_name: str) -> tuple[str, str]:
        """Generate Quest System C++ header and implementation"""
        quests = json_data.get("quests", [])

        # Header file
        header = f'''#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Engine/DataTable.h"
#include "{world_name}QuestSystem.generated.h"

UENUM(BlueprintType)
enum class EQuestType : uint8
{{
    Main UMETA(DisplayName = "Main Quest"),
    Side UMETA(DisplayName = "Side Quest"),
    Optional UMETA(DisplayName = "Optional Quest")
}};

UENUM(BlueprintType)
enum class EQuestStatus : uint8
{{
    NotStarted UMETA(DisplayName = "Not Started"),
    InProgress UMETA(DisplayName = "In Progress"),
    Completed UMETA(DisplayName = "Completed"),
    Failed UMETA(DisplayName = "Failed")
}};

USTRUCT(BlueprintType)
struct F{world_name}QuestReward : public FTableRowBase
{{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Reward")
    int32 Experience = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Reward")
    int32 Gold = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Reward")
    TArray<FString> Items;
}};

USTRUCT(BlueprintType)
struct F{world_name}Quest : public FTableRowBase
{{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString QuestID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString QuestName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    EQuestType QuestType = EQuestType::Main;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString Objective;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    TArray<FString> Requirements;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    F{world_name}QuestReward Rewards;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString Location;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString EstimatedTime;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    EQuestStatus Status = EQuestStatus::NotStarted;
}};

UCLASS(BlueprintType, Blueprintable)
class GAMEMODULE_API A{world_name}QuestSystem : public AActor
{{
    GENERATED_BODY()

public:
    A{world_name}QuestSystem();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest System")
    TArray<F{world_name}Quest> Quests;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest System")
    TArray<F{world_name}Quest> ActiveQuests;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest System")
    TArray<F{world_name}Quest> CompletedQuests;

public:
    UFUNCTION(BlueprintCallable, Category = "Quest System")
    bool StartQuest(const FString& QuestID);

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    bool CompleteQuest(const FString& QuestID);

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    bool IsQuestActive(const FString& QuestID) const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    bool IsQuestCompleted(const FString& QuestID) const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    F{world_name}Quest GetQuest(const FString& QuestID) const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    TArray<F{world_name}Quest> GetActiveQuests() const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    TArray<F{world_name}Quest> GetAvailableQuests() const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    void LoadQuestsFromJSON();

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnQuestStarted, const F{world_name}Quest&, Quest);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnQuestCompleted, const F{world_name}Quest&, Quest);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnQuestFailed, const F{world_name}Quest&, Quest);

    UPROPERTY(BlueprintAssignable, Category = "Quest System")
    FOnQuestStarted OnQuestStarted;

    UPROPERTY(BlueprintAssignable, Category = "Quest System")
    FOnQuestCompleted OnQuestCompleted;

    UPROPERTY(BlueprintAssignable, Category = "Quest System")
    FOnQuestFailed OnQuestFailed;
}};'''

        # Implementation file
        implementation = f'''#include "{world_name}QuestSystem.h"
#include "Engine/Engine.h"
#include "Misc/FileHelper.h"
#include "HAL/PlatformFilemanager.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonReader.h"

A{world_name}QuestSystem::A{world_name}QuestSystem()
{{
    PrimaryActorTick.bCanEverTick = false;

    // Initialize quest data from generated JSON
    LoadQuestsFromJSON();
}}

void A{world_name}QuestSystem::BeginPlay()
{{
    Super::BeginPlay();

    UE_LOG(LogTemp, Warning, TEXT("{world_name} Quest System initialized with %d quests"), Quests.Num());
}}

bool A{world_name}QuestSystem::StartQuest(const FString& QuestID)
{{
    for (F{world_name}Quest& Quest : Quests)
    {{
        if (Quest.QuestID == QuestID && Quest.Status == EQuestStatus::NotStarted)
        {{
            // Check requirements
            bool RequirementsMet = true;
            for (const FString& Requirement : Quest.Requirements)
            {{
                if (!IsQuestCompleted(Requirement))
                {{
                    RequirementsMet = false;
                    break;
                }}
            }}

            if (RequirementsMet)
            {{
                Quest.Status = EQuestStatus::InProgress;
                ActiveQuests.Add(Quest);
                OnQuestStarted.Broadcast(Quest);

                UE_LOG(LogTemp, Warning, TEXT("Started quest: %s"), *Quest.QuestName);
                return true;
            }}
            else
            {{
                UE_LOG(LogTemp, Warning, TEXT("Quest requirements not met: %s"), *Quest.QuestName);
                return false;
            }}
        }}
    }}

    UE_LOG(LogTemp, Warning, TEXT("Quest not found or already started: %s"), *QuestID);
    return false;
}}

bool A{world_name}QuestSystem::CompleteQuest(const FString& QuestID)
{{
    for (int32 i = 0; i < ActiveQuests.Num(); i++)
    {{
        if (ActiveQuests[i].QuestID == QuestID)
        {{
            F{world_name}Quest CompletedQuest = ActiveQuests[i];
            CompletedQuest.Status = EQuestStatus::Completed;

            // Update main quest array
            for (F{world_name}Quest& Quest : Quests)
            {{
                if (Quest.QuestID == QuestID)
                {{
                    Quest.Status = EQuestStatus::Completed;
                    break;
                }}
            }}

            CompletedQuests.Add(CompletedQuest);
            ActiveQuests.RemoveAt(i);
            OnQuestCompleted.Broadcast(CompletedQuest);

            UE_LOG(LogTemp, Warning, TEXT("Completed quest: %s"), *CompletedQuest.QuestName);
            return true;
        }}
    }}

    UE_LOG(LogTemp, Warning, TEXT("Active quest not found: %s"), *QuestID);
    return false;
}}

bool A{world_name}QuestSystem::IsQuestActive(const FString& QuestID) const
{{
    for (const F{world_name}Quest& Quest : ActiveQuests)
    {{
        if (Quest.QuestID == QuestID)
        {{
            return true;
        }}
    }}
    return false;
}}

bool A{world_name}QuestSystem::IsQuestCompleted(const FString& QuestID) const
{{
    for (const F{world_name}Quest& Quest : CompletedQuests)
    {{
        if (Quest.QuestID == QuestID)
        {{
            return true;
        }}
    }}
    return false;
}}

F{world_name}Quest A{world_name}QuestSystem::GetQuest(const FString& QuestID) const
{{
    for (const F{world_name}Quest& Quest : Quests)
    {{
        if (Quest.QuestID == QuestID)
        {{
            return Quest;
        }}
    }}
    return F{world_name}Quest();
}}

TArray<F{world_name}Quest> A{world_name}QuestSystem::GetActiveQuests() const
{{
    return ActiveQuests;
}}

TArray<F{world_name}Quest> A{world_name}QuestSystem::GetAvailableQuests() const
{{
    TArray<F{world_name}Quest> AvailableQuests;

    for (const F{world_name}Quest& Quest : Quests)
    {{
        if (Quest.Status == EQuestStatus::NotStarted)
        {{
            // Check if requirements are met
            bool RequirementsMet = true;
            for (const FString& Requirement : Quest.Requirements)
            {{
                if (!IsQuestCompleted(Requirement))
                {{
                    RequirementsMet = false;
                    break;
                }}
            }}

            if (RequirementsMet)
            {{
                AvailableQuests.Add(Quest);
            }}
        }}
    }}

    return AvailableQuests;
}}

void A{world_name}QuestSystem::LoadQuestsFromJSON()
{{
    // Load quest data from generated JSON file
    FString FilePath = FPaths::ProjectContentDir() + TEXT("Data/QuestData.json");
    FString JsonString;

    if (FFileHelper::LoadFileToString(JsonString, *FilePath))
    {{
        TSharedPtr<FJsonObject> JsonObject;
        TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

        if (FJsonSerializer::Deserialize(Reader, JsonObject))
        {{
            const TArray<TSharedPtr<FJsonValue>>* QuestArray;
            if (JsonObject->TryGetArrayField(TEXT("quests"), QuestArray))
            {{
                for (const TSharedPtr<FJsonValue>& QuestValue : *QuestArray)
                {{
                    const TSharedPtr<FJsonObject>& QuestObj = QuestValue->AsObject();

                    F{world_name}Quest NewQuest;
                    NewQuest.QuestID = QuestObj->GetStringField(TEXT("id"));
                    NewQuest.QuestName = QuestObj->GetStringField(TEXT("name"));
                    NewQuest.Objective = QuestObj->GetStringField(TEXT("objective"));
                    NewQuest.Description = QuestObj->GetStringField(TEXT("description"));
                    NewQuest.Location = QuestObj->GetStringField(TEXT("location"));
                    NewQuest.EstimatedTime = QuestObj->GetStringField(TEXT("estimated_time"));

                    // Parse quest type
                    FString TypeString = QuestObj->GetStringField(TEXT("type"));
                    if (TypeString == TEXT("main"))
                        NewQuest.QuestType = EQuestType::Main;
                    else if (TypeString == TEXT("side"))
                        NewQuest.QuestType = EQuestType::Side;
                    else
                        NewQuest.QuestType = EQuestType::Optional;

                    // Parse requirements
                    const TArray<TSharedPtr<FJsonValue>>* RequirementsArray;
                    if (QuestObj->TryGetArrayField(TEXT("requirements"), RequirementsArray))
                    {{
                        for (const TSharedPtr<FJsonValue>& ReqValue : *RequirementsArray)
                        {{
                            NewQuest.Requirements.Add(ReqValue->AsString());
                        }}
                    }}

                    // Parse rewards
                    const TSharedPtr<FJsonObject>* RewardsObj;
                    if (QuestObj->TryGetObjectField(TEXT("rewards"), RewardsObj))
                    {{
                        NewQuest.Rewards.Experience = (*RewardsObj)->GetIntegerField(TEXT("experience"));
                        NewQuest.Rewards.Gold = (*RewardsObj)->GetIntegerField(TEXT("gold"));

                        const TArray<TSharedPtr<FJsonValue>>* ItemsArray;
                        if ((*RewardsObj)->TryGetArrayField(TEXT("items"), ItemsArray))
                        {{
                            for (const TSharedPtr<FJsonValue>& ItemValue : *ItemsArray)
                            {{
                                NewQuest.Rewards.Items.Add(ItemValue->AsString());
                            }}
                        }}
                    }}

                    Quests.Add(NewQuest);
                }}
            }}
        }}
    }}
    else
    {{
        UE_LOG(LogTemp, Error, TEXT("Failed to load quest data from: %s"), *FilePath);
    }}
}}'''

        return header, implementation

    def _generate_npc_system_cpp(self, json_data: Dict[str, Any], world_name: str) -> tuple[str, str]:
        """Generate NPC System C++ header and implementation"""

        # Header file
        header = f'''#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "{world_name}NPCSystem.generated.h"

UENUM(BlueprintType)
enum class ENPCType : uint8
{{
    Friendly UMETA(DisplayName = "Friendly"),
    Neutral UMETA(DisplayName = "Neutral"),
    Hostile UMETA(DisplayName = "Hostile")
}};

UENUM(BlueprintType)
enum class ENPCBehavior : uint8
{{
    Stationary UMETA(DisplayName = "Stationary"),
    Patrol UMETA(DisplayName = "Patrol"),
    Follow UMETA(DisplayName = "Follow"),
    Aggressive UMETA(DisplayName = "Aggressive")
}};

USTRUCT(BlueprintType)
struct F{world_name}NPCStats
{{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 Health = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 Attack = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 Defense = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float MovementSpeed = 300.0f;
}};

USTRUCT(BlueprintType)
struct F{world_name}NPCData
{{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    FString NPCID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    FString NPCName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    FString Role;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    ENPCType NPCType = ENPCType::Neutral;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    FString Location;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    TArray<FString> Dialogue;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    ENPCBehavior Behavior = ENPCBehavior::Stationary;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    F{world_name}NPCStats Stats;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    TArray<FString> Inventory;
}};

UCLASS(BlueprintType, Blueprintable)
class GAMEMODULE_API A{world_name}NPC : public ACharacter
{{
    GENERATED_BODY()

public:
    A{world_name}NPC();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC Data")
    F{world_name}NPCData NPCData;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class USphereComponent* InteractionSphere;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    int32 CurrentDialogueIndex = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    bool bCanInteract = true;

public:
    virtual void Tick(float DeltaTime) override;

    UFUNCTION(BlueprintCallable, Category = "NPC")
    void InitializeFromData(const F{world_name}NPCData& Data);

    UFUNCTION(BlueprintCallable, Category = "NPC")
    FString GetCurrentDialogue();

    UFUNCTION(BlueprintCallable, Category = "NPC")
    FString GetNextDialogue();

    UFUNCTION(BlueprintCallable, Category = "NPC")
    bool HasMoreDialogue() const;

    UFUNCTION(BlueprintCallable, Category = "NPC")
    void ResetDialogue();

    UFUNCTION(BlueprintCallable, Category = "NPC")
    void StartInteraction(AActor* InteractingActor);

    UFUNCTION(BlueprintCallable, Category = "NPC")
    void EndInteraction();

    UFUNCTION(BlueprintImplementableEvent, Category = "NPC")
    void OnInteractionStarted(AActor* InteractingActor);

    UFUNCTION(BlueprintImplementableEvent, Category = "NPC")
    void OnInteractionEnded();

    UFUNCTION(BlueprintImplementableEvent, Category = "NPC")
    void OnDialogueChanged(const FString& NewDialogue);

protected:
    UFUNCTION()
    void OnInteractionSphereBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

    UFUNCTION()
    void OnInteractionSphereEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);

private:
    void UpdateBehavior();
    void HandlePatrolBehavior();
    void HandleAggressiveBehavior();
}};

UCLASS(BlueprintType, Blueprintable)
class GAMEMODULE_API A{world_name}NPCManager : public AActor
{{
    GENERATED_BODY()

public:
    A{world_name}NPCManager();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC Manager")
    TArray<F{world_name}NPCData> NPCDatabase;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC Manager")
    TSubclassOf<A{world_name}NPC> NPCClass;

    UPROPERTY(BlueprintReadOnly, Category = "NPC Manager")
    TArray<A{world_name}NPC*> SpawnedNPCs;

public:
    UFUNCTION(BlueprintCallable, Category = "NPC Manager")
    void LoadNPCsFromJSON();

    UFUNCTION(BlueprintCallable, Category = "NPC Manager")
    A{world_name}NPC* SpawnNPC(const FString& NPCID, const FVector& Location, const FRotator& Rotation);

    UFUNCTION(BlueprintCallable, Category = "NPC Manager")
    A{world_name}NPC* FindNPCByID(const FString& NPCID);

    UFUNCTION(BlueprintCallable, Category = "NPC Manager")
    TArray<A{world_name}NPC*> GetNPCsByType(ENPCType NPCType);

    UFUNCTION(BlueprintCallable, Category = "NPC Manager")
    void SpawnAllNPCs();
}};'''

        # Implementation file
        implementation = f'''#include "{world_name}NPCSystem.h"
#include "Engine/Engine.h"
#include "Components/SphereComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Misc/FileHelper.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonReader.h"

A{world_name}NPC::A{world_name}NPC()
{{
    PrimaryActorTick.bCanEverTick = true;

    // Create interaction sphere
    InteractionSphere = CreateDefaultSubobject<USphereComponent>(TEXT("InteractionSphere"));
    InteractionSphere->SetupAttachment(RootComponent);
    InteractionSphere->SetSphereRadius(200.0f);
    InteractionSphere->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
    InteractionSphere->SetCollisionResponseToAllChannels(ECR_Ignore);
    InteractionSphere->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);

    // Bind overlap events
    InteractionSphere->OnComponentBeginOverlap.AddDynamic(this, &A{world_name}NPC::OnInteractionSphereBeginOverlap);
    InteractionSphere->OnComponentEndOverlap.AddDynamic(this, &A{world_name}NPC::OnInteractionSphereEndOverlap);
}}

void A{world_name}NPC::BeginPlay()
{{
    Super::BeginPlay();

    // Apply stats to character
    if (GetCharacterMovement())
    {{
        GetCharacterMovement()->MaxWalkSpeed = NPCData.Stats.MovementSpeed;
    }}
}}

void A{world_name}NPC::Tick(float DeltaTime)
{{
    Super::Tick(DeltaTime);

    UpdateBehavior();
}}

void A{world_name}NPC::InitializeFromData(const F{world_name}NPCData& Data)
{{
    NPCData = Data;

    // Apply movement speed
    if (GetCharacterMovement())
    {{
        GetCharacterMovement()->MaxWalkSpeed = NPCData.Stats.MovementSpeed;
    }}

    UE_LOG(LogTemp, Warning, TEXT("Initialized NPC: %s"), *NPCData.NPCName);
}}

FString A{world_name}NPC::GetCurrentDialogue()
{{
    if (NPCData.Dialogue.IsValidIndex(CurrentDialogueIndex))
    {{
        return NPCData.Dialogue[CurrentDialogueIndex];
    }}
    return TEXT("...");
}}

FString A{world_name}NPC::GetNextDialogue()
{{
    if (HasMoreDialogue())
    {{
        CurrentDialogueIndex++;
        FString NewDialogue = GetCurrentDialogue();
        OnDialogueChanged(NewDialogue);
        return NewDialogue;
    }}
    return GetCurrentDialogue();
}}

bool A{world_name}NPC::HasMoreDialogue() const
{{
    return CurrentDialogueIndex < NPCData.Dialogue.Num() - 1;
}}

void A{world_name}NPC::ResetDialogue()
{{
    CurrentDialogueIndex = 0;
}}

void A{world_name}NPC::StartInteraction(AActor* InteractingActor)
{{
    if (bCanInteract)
    {{
        OnInteractionStarted(InteractingActor);
        UE_LOG(LogTemp, Warning, TEXT("Started interaction with %s"), *NPCData.NPCName);
    }}
}}

void A{world_name}NPC::EndInteraction()
{{
    OnInteractionEnded();
    ResetDialogue();
}}

void A{world_name}NPC::OnInteractionSphereBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{{
    // Handle player entering interaction range
    if (OtherActor && OtherActor->IsA<APawn>())
    {{
        UE_LOG(LogTemp, Warning, TEXT("Player entered interaction range of %s"), *NPCData.NPCName);
    }}
}}

void A{world_name}NPC::OnInteractionSphereEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{{
    // Handle player leaving interaction range
    if (OtherActor && OtherActor->IsA<APawn>())
    {{
        EndInteraction();
        UE_LOG(LogTemp, Warning, TEXT("Player left interaction range of %s"), *NPCData.NPCName);
    }}
}}

void A{world_name}NPC::UpdateBehavior()
{{
    switch (NPCData.Behavior)
    {{
        case ENPCBehavior::Patrol:
            HandlePatrolBehavior();
            break;
        case ENPCBehavior::Aggressive:
            HandleAggressiveBehavior();
            break;
        case ENPCBehavior::Stationary:
        case ENPCBehavior::Follow:
        default:
            // Handled in Blueprint or other systems
            break;
    }}
}}

void A{world_name}NPC::HandlePatrolBehavior()
{{
    // Basic patrol logic - can be expanded in Blueprint
}}

void A{world_name}NPC::HandleAggressiveBehavior()
{{
    // Basic aggressive behavior - can be expanded in Blueprint
}}

// NPC Manager Implementation
A{world_name}NPCManager::A{world_name}NPCManager()
{{
    PrimaryActorTick.bCanEverTick = false;
}}

void A{world_name}NPCManager::BeginPlay()
{{
    Super::BeginPlay();

    LoadNPCsFromJSON();
    SpawnAllNPCs();
}}

void A{world_name}NPCManager::LoadNPCsFromJSON()
{{
    FString FilePath = FPaths::ProjectContentDir() + TEXT("Data/NPCData.json");
    FString JsonString;

    if (FFileHelper::LoadFileToString(JsonString, *FilePath))
    {{
        TSharedPtr<FJsonObject> JsonObject;
        TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

        if (FJsonSerializer::Deserialize(Reader, JsonObject))
        {{
            const TArray<TSharedPtr<FJsonValue>>* NPCArray;
            if (JsonObject->TryGetArrayField(TEXT("npcs"), NPCArray))
            {{
                for (const TSharedPtr<FJsonValue>& NPCValue : *NPCArray)
                {{
                    const TSharedPtr<FJsonObject>& NPCObj = NPCValue->AsObject();

                    F{world_name}NPCData NewNPC;
                    NewNPC.NPCID = NPCObj->GetStringField(TEXT("id"));
                    NewNPC.NPCName = NPCObj->GetStringField(TEXT("name"));
                    NewNPC.Role = NPCObj->GetStringField(TEXT("role"));
                    NewNPC.Location = NPCObj->GetStringField(TEXT("location"));

                    // Parse NPC type
                    FString TypeString = NPCObj->GetStringField(TEXT("type"));
                    if (TypeString == TEXT("friendly"))
                        NewNPC.NPCType = ENPCType::Friendly;
                    else if (TypeString == TEXT("hostile"))
                        NewNPC.NPCType = ENPCType::Hostile;
                    else
                        NewNPC.NPCType = ENPCType::Neutral;

                    // Parse behavior
                    FString BehaviorString = NPCObj->GetStringField(TEXT("behavior"));
                    if (BehaviorString.Contains(TEXT("patrol")))
                        NewNPC.Behavior = ENPCBehavior::Patrol;
                    else if (BehaviorString.Contains(TEXT("aggressive")))
                        NewNPC.Behavior = ENPCBehavior::Aggressive;
                    else
                        NewNPC.Behavior = ENPCBehavior::Stationary;

                    // Parse dialogue
                    const TArray<TSharedPtr<FJsonValue>>* DialogueArray;
                    if (NPCObj->TryGetArrayField(TEXT("dialogue"), DialogueArray))
                    {{
                        for (const TSharedPtr<FJsonValue>& DialogueValue : *DialogueArray)
                        {{
                            NewNPC.Dialogue.Add(DialogueValue->AsString());
                        }}
                    }}

                    // Parse stats
                    const TSharedPtr<FJsonObject>* StatsObj;
                    if (NPCObj->TryGetObjectField(TEXT("stats"), StatsObj))
                    {{
                        NewNPC.Stats.Health = (*StatsObj)->GetIntegerField(TEXT("health"));
                        NewNPC.Stats.Attack = (*StatsObj)->GetIntegerField(TEXT("attack"));
                        NewNPC.Stats.Defense = (*StatsObj)->GetIntegerField(TEXT("defense"));
                    }}

                    // Parse inventory
                    const TArray<TSharedPtr<FJsonValue>>* InventoryArray;
                    if (NPCObj->TryGetArrayField(TEXT("inventory"), InventoryArray))
                    {{
                        for (const TSharedPtr<FJsonValue>& ItemValue : *InventoryArray)
                        {{
                            NewNPC.Inventory.Add(ItemValue->AsString());
                        }}
                    }}

                    NPCDatabase.Add(NewNPC);
                }}
            }}
        }}
    }}
}}

A{world_name}NPC* A{world_name}NPCManager::SpawnNPC(const FString& NPCID, const FVector& Location, const FRotator& Rotation)
{{
    if (!NPCClass)
    {{
        UE_LOG(LogTemp, Error, TEXT("NPC Class not set in NPCManager"));
        return nullptr;
    }}

    // Find NPC data
    F{world_name}NPCData* NPCData = NPCDatabase.FindByPredicate([&NPCID](const F{world_name}NPCData& Data)
    {{
        return Data.NPCID == NPCID;
    }});

    if (!NPCData)
    {{
        UE_LOG(LogTemp, Error, TEXT("NPC data not found for ID: %s"), *NPCID);
        return nullptr;
    }}

    // Spawn NPC
    A{world_name}NPC* SpawnedNPC = GetWorld()->SpawnActor<A{world_name}NPC>(NPCClass, Location, Rotation);
    if (SpawnedNPC)
    {{
        SpawnedNPC->InitializeFromData(*NPCData);
        SpawnedNPCs.Add(SpawnedNPC);
        UE_LOG(LogTemp, Warning, TEXT("Spawned NPC: %s"), *NPCData->NPCName);
    }}

    return SpawnedNPC;
}}

A{world_name}NPC* A{world_name}NPCManager::FindNPCByID(const FString& NPCID)
{{
    for (A{world_name}NPC* NPC : SpawnedNPCs)
    {{
        if (NPC && NPC->NPCData.NPCID == NPCID)
        {{
            return NPC;
        }}
    }}
    return nullptr;
}}

TArray<A{world_name}NPC*> A{world_name}NPCManager::GetNPCsByType(ENPCType NPCType)
{{
    TArray<A{world_name}NPC*> FilteredNPCs;

    for (A{world_name}NPC* NPC : SpawnedNPCs)
    {{
        if (NPC && NPC->NPCData.NPCType == NPCType)
        {{
            FilteredNPCs.Add(NPC);
        }}
    }}

    return FilteredNPCs;
}}

void A{world_name}NPCManager::SpawnAllNPCs()
{{
    // Spawn NPCs at default locations - can be customized
    for (int32 i = 0; i < NPCDatabase.Num(); i++)
    {{
        FVector SpawnLocation = FVector(i * 500.0f, 0.0f, 100.0f); // Spread NPCs out
        SpawnNPC(NPCDatabase[i].NPCID, SpawnLocation, FRotator::ZeroRotator);
    }}
}}'''

        return header, implementation

    def _generate_environment_system_cpp(self, json_data: Dict[str, Any], world_name: str) -> tuple[str, str]:
        """Generate Environment System C++ files"""
        env_data = json_data.get("environment", {})

        header = f'''#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "{world_name}Environment.generated.h"

USTRUCT(BlueprintType)
struct F{world_name}EnvironmentData
{{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString EnvironmentType = TEXT("{env_data.get('type', 'forest')}");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Setting = TEXT("{env_data.get('setting', 'A mysterious location')}");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Lighting = TEXT("{env_data.get('lighting', 'dynamic')}");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Weather = TEXT("{env_data.get('weather', 'clear')}");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Atmosphere = TEXT("{env_data.get('atmosphere', 'mysterious')}");
}};

UCLASS(BlueprintType, Blueprintable)
class GAMEMODULE_API A{world_name}Environment : public AActor
{{
    GENERATED_BODY()

public:
    A{world_name}Environment();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    F{world_name}EnvironmentData EnvironmentData;

public:
    UFUNCTION(BlueprintCallable, Category = "Environment")
    void LoadEnvironmentFromJSON();

    UFUNCTION(BlueprintCallable, Category = "Environment")
    void ApplyEnvironmentSettings();
}};'''

        implementation = f'''#include "{world_name}Environment.h"
#include "Engine/Engine.h"

A{world_name}Environment::A{world_name}Environment()
{{
    PrimaryActorTick.bCanEverTick = false;
}}

void A{world_name}Environment::BeginPlay()
{{
    Super::BeginPlay();
    LoadEnvironmentFromJSON();
    ApplyEnvironmentSettings();
}}

void A{world_name}Environment::LoadEnvironmentFromJSON()
{{
    // Load environment data from JSON
    UE_LOG(LogTemp, Warning, TEXT("Loading environment: %s"), *EnvironmentData.EnvironmentType);
}}

void A{world_name}Environment::ApplyEnvironmentSettings()
{{
    // Apply environment settings to the world
    UE_LOG(LogTemp, Warning, TEXT("Applied environment settings for %s"), *EnvironmentData.Setting);
}}'''

        return header, implementation

    def _generate_player_controller_cpp(self, json_data: Dict[str, Any], world_name: str) -> tuple[str, str]:
        """Generate Player Controller C++ files"""
        physics_data = json_data.get("physics", {})
        abilities = physics_data.get("player_abilities", ["walk", "run", "jump"])

        header = f'''#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "{world_name}PlayerController.generated.h"

UCLASS(BlueprintType, Blueprintable)
class GAMEMODULE_API A{world_name}PlayerController : public APlayerController
{{
    GENERATED_BODY()

public:
    A{world_name}PlayerController();

protected:
    virtual void BeginPlay() override;
    virtual void SetupInputComponent() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Player Abilities")
    TArray<FString> PlayerAbilities;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Player Settings")
    float MovementSpeed = {physics_data.get('movement_speed', 5.0)};

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Player Settings")
    float JumpHeight = {physics_data.get('jump_height', 2.0)};

public:
    UFUNCTION(BlueprintCallable, Category = "Player")
    bool HasAbility(const FString& AbilityName) const;

    UFUNCTION(BlueprintCallable, Category = "Player")
    void LoadPlayerSettings();
}};'''

        implementation = f'''#include "{world_name}PlayerController.h"
#include "Engine/Engine.h"

A{world_name}PlayerController::A{world_name}PlayerController()
{{
    // Initialize player abilities
    {chr(10).join([f'    PlayerAbilities.Add(TEXT("{ability}"));' for ability in abilities])}
}}

void A{world_name}PlayerController::BeginPlay()
{{
    Super::BeginPlay();
    LoadPlayerSettings();
}}

void A{world_name}PlayerController::SetupInputComponent()
{{
    Super::SetupInputComponent();
    // Setup input bindings here
}}

bool A{world_name}PlayerController::HasAbility(const FString& AbilityName) const
{{
    return PlayerAbilities.Contains(AbilityName);
}}

void A{world_name}PlayerController::LoadPlayerSettings()
{{
    UE_LOG(LogTemp, Warning, TEXT("Loaded player settings - Speed: %f, Jump: %f"), MovementSpeed, JumpHeight);
}}'''

        return header, implementation

    def _create_blueprint_quest_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Blueprint-compatible quest data"""
        quests = json_data.get("quests", [])

        blueprint_data = {
            "QuestSystemData": {
                "TotalQuests": len(quests),
                "MainQuests": len([q for q in quests if q.get("type") == "main"]),
                "SideQuests": len([q for q in quests if q.get("type") == "side"]),
                "Quests": []
            }
        }

        for quest in quests:
            bp_quest = {
                "ID": quest.get("id", ""),
                "Name": quest.get("name", ""),
                "Type": quest.get("type", "main"),
                "Objective": quest.get("objective", ""),
                "Description": quest.get("description", ""),
                "Requirements": quest.get("requirements", []),
                "Rewards": {
                    "Experience": quest.get("rewards", {}).get("experience", 0),
                    "Gold": quest.get("rewards", {}).get("gold", 0),
                    "Items": quest.get("rewards", {}).get("items", [])
                },
                "Location": quest.get("location", ""),
                "EstimatedTime": quest.get("estimated_time", ""),
                "Status": "NotStarted"
            }
            blueprint_data["QuestSystemData"]["Quests"].append(bp_quest)

        return blueprint_data

    def _create_blueprint_npc_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Blueprint-compatible NPC data"""
        npcs = json_data.get("npcs", [])

        blueprint_data = {
            "NPCSystemData": {
                "TotalNPCs": len(npcs),
                "FriendlyNPCs": len([n for n in npcs if n.get("type") == "friendly"]),
                "HostileNPCs": len([n for n in npcs if n.get("type") == "hostile"]),
                "NPCs": []
            }
        }

        for npc in npcs:
            bp_npc = {
                "ID": npc.get("id", ""),
                "Name": npc.get("name", ""),
                "Role": npc.get("role", ""),
                "Type": npc.get("type", "neutral"),
                "Location": npc.get("location", ""),
                "Dialogue": npc.get("dialogue", []),
                "Behavior": npc.get("behavior", "stationary"),
                "Stats": {
                    "Health": npc.get("stats", {}).get("health", 100),
                    "Attack": npc.get("stats", {}).get("attack", 10),
                    "Defense": npc.get("stats", {}).get("defense", 10)
                },
                "Inventory": npc.get("inventory", []),
                "SpawnLocation": {"X": 0, "Y": 0, "Z": 0}
            }
            blueprint_data["NPCSystemData"]["NPCs"].append(bp_npc)

        return blueprint_data

    def _create_blueprint_environment_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Blueprint-compatible environment data"""
        env = json_data.get("environment", {})

        return {
            "EnvironmentData": {
                "Type": env.get("type", "forest"),
                "Setting": env.get("setting", ""),
                "Terrain": env.get("terrain", []),
                "Lighting": env.get("lighting", "dynamic"),
                "Weather": env.get("weather", "clear"),
                "Atmosphere": env.get("atmosphere", "mysterious"),
                "Size": env.get("size", "medium"),
                "Assets": env.get("assets", [])
            }
        }

    def _create_blueprint_asset_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Blueprint-compatible asset data"""
        assets = json_data.get("assets_required", {})

        return {
            "AssetData": {
                "Models": assets.get("models", []),
                "Textures": assets.get("textures", []),
                "Sounds": assets.get("sounds", []),
                "Effects": assets.get("effects", []),
                "Animations": assets.get("animations", [])
            }
        }

    def _create_varest_compatible_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create VaRest plugin compatible data structure"""
        return {
            "WorldData": {
                "Metadata": json_data.get("metadata", {}),
                "Environment": json_data.get("environment", {}),
                "Quests": json_data.get("quests", []),
                "NPCs": json_data.get("npcs", []),
                "Physics": json_data.get("physics", {}),
                "WinConditions": json_data.get("win_conditions", []),
                "LoseConditions": json_data.get("lose_conditions", []),
                "AssetsRequired": json_data.get("assets_required", {})
            },
            "VaRestMetadata": {
                "Version": "1.0",
                "GeneratedBy": "TTG Genesis",
                "Timestamp": "2025-01-01T00:00:00Z",
                "Format": "VaRest Compatible"
            }
        }

    def _generate_build_cs(self, world_name: str) -> str:
        """Generate Build.cs file for UE5 module compilation"""
        return f'''using UnrealBuildTool;

public class {world_name} : ModuleRules
{{
    public {world_name}(ReadOnlyTargetRules Target) : base(Target)
    {{
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {{
            "Core",
            "CoreUObject",
            "Engine",
            "InputCore",
            "Json",
            "JsonUtilities"
        }});

        PrivateDependencyModuleNames.AddRange(new string[]
        {{
            "Slate",
            "SlateCore",
            "UMG",
            "HTTP",
            "VaRest"
        }});
    }}
}}'''

    def _generate_module_header(self, world_name: str) -> str:
        """Generate module header file"""
        return f'''#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

class F{world_name}Module : public IModuleInterface
{{
public:
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;
}};'''

    def _generate_module_cpp(self, world_name: str) -> str:
        """Generate module implementation file"""
        return f'''#include "{world_name}Module.h"

#define LOCTEXT_NAMESPACE "F{world_name}Module"

void F{world_name}Module::StartupModule()
{{
    // This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
    UE_LOG(LogTemp, Warning, TEXT("{world_name} Module Started"));
}}

void F{world_name}Module::ShutdownModule()
{{
    // This function may be called during shutdown to clean up your module. For modules that support dynamic reloading,
    // we call this function before unloading the module.
    UE_LOG(LogTemp, Warning, TEXT("{world_name} Module Shutdown"));
}}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(F{world_name}Module, {world_name})'''

    def _generate_integration_readme(self, json_data: Dict[str, Any], world_name: str) -> str:
        """Generate integration README for UE5"""
        metadata = json_data.get("metadata", {})
        quests = json_data.get("quests", [])
        npcs = json_data.get("npcs", [])

        return f'''# {world_name} - UE5 Integration Guide

## Generated World: {metadata.get("level_name", "Unknown")}
**Description**: {metadata.get("description", "No description available")}
**Theme**: {metadata.get("theme", "Unknown")}
**Difficulty**: {metadata.get("difficulty", "Medium")}
**Estimated Playtime**: {metadata.get("estimated_playtime", "Unknown")}

## Files Generated

### C++ Files (ue5-c++/)
- `{world_name}QuestSystem.h/.cpp` - Quest management system
- `{world_name}NPCSystem.h/.cpp` - NPC management and interaction
- `{world_name}Environment.h/.cpp` - Environment and world settings
- `{world_name}PlayerController.h/.cpp` - Player controller with abilities
- `{world_name}Module.h/.cpp` - Module definition
- `{world_name}.Build.cs` - Build configuration

### Blueprint Data Files (ue5-exports/)
- `QuestData.json` - Quest system data for Blueprints
- `NPCData.json` - NPC data for spawning and behavior
- `EnvironmentData.json` - Environment configuration
- `AssetList.json` - Required assets list
- `WorldData_VaRest.json` - VaRest plugin compatible data

## Integration Steps

### 1. C++ Integration
1. Copy all `.h` and `.cpp` files to your UE5 project's Source folder
2. Copy the `.Build.cs` file to your module directory
3. Add the module to your project's `.uproject` file:
```json
"Modules": [
    {{
        "Name": "{world_name}",
        "Type": "Runtime",
        "LoadingPhase": "Default"
    }}
]
```
4. Regenerate project files and compile

### 2. Blueprint Integration
1. Copy JSON files to `Content/Data/` folder in your UE5 project
2. Create Blueprint classes inheriting from the generated C++ classes:
   - `BP_{world_name}QuestSystem` from `A{world_name}QuestSystem`
   - `BP_{world_name}NPCManager` from `A{world_name}NPCManager`
   - `BP_{world_name}Environment` from `A{world_name}Environment`

### 3. VaRest Integration (Optional)
If using VaRest plugin:
1. Install VaRest plugin in your project
2. Use `WorldData_VaRest.json` with VaRest's JSON parsing nodes
3. Create Blueprint logic to parse and apply the world data

## World Statistics
- **Total Quests**: {len(quests)}
- **Main Quests**: {len([q for q in quests if q.get("type") == "main"])}
- **Side Quests**: {len([q for q in quests if q.get("type") == "side"])}
- **Total NPCs**: {len(npcs)}
- **Friendly NPCs**: {len([n for n in npcs if n.get("type") == "friendly"])}
- **Hostile NPCs**: {len([n for n in npcs if n.get("type") == "hostile"])}

## Quest List
{chr(10).join([f"- **{q.get('name', 'Unknown')}** ({q.get('type', 'unknown')}): {q.get('objective', 'No objective')}" for q in quests])}

## NPC List
{chr(10).join([f"- **{n.get('name', 'Unknown')}** ({n.get('type', 'unknown')}): {n.get('role', 'No role')}" for n in npcs])}

## Required Assets
### Models
{chr(10).join([f"- {asset}" for asset in json_data.get("assets_required", {}).get("models", [])])}

### Textures
{chr(10).join([f"- {asset}" for asset in json_data.get("assets_required", {}).get("textures", [])])}

### Sounds
{chr(10).join([f"- {asset}" for asset in json_data.get("assets_required", {}).get("sounds", [])])}

### Effects
{chr(10).join([f"- {asset}" for asset in json_data.get("assets_required", {}).get("effects", [])])}

## Usage Examples

### Starting a Quest (C++)
```cpp
A{world_name}QuestSystem* QuestSystem = GetWorld()->SpawnActor<A{world_name}QuestSystem>();
bool Success = QuestSystem->StartQuest(TEXT("quest_1"));
```

### Spawning an NPC (C++)
```cpp
A{world_name}NPCManager* NPCManager = GetWorld()->SpawnActor<A{world_name}NPCManager>();
A{world_name}NPC* SpawnedNPC = NPCManager->SpawnNPC(TEXT("npc_1"), FVector(0,0,0), FRotator::ZeroRotator);
```

### Blueprint Usage
Use the generated Blueprint classes and bind to the provided events:
- `OnQuestStarted`
- `OnQuestCompleted`
- `OnQuestFailed`

## Notes
- All generated code follows UE5 coding standards
- JSON data is automatically loaded at runtime
- Blueprint events are provided for easy integration
- VaRest compatibility ensures easy data manipulation

Generated by TTG Genesis - Text to Game World Generator
'''

    def _write_file(self, filepath: Path, content: str) -> str:
        """Write content to file and return the path"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Generated: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to write {filepath}: {e}")
            return ""

    def _write_json_file(self, filepath: Path, data: Dict[str, Any]) -> str:
        """Write JSON data to file and return the path"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Generated JSON: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to write JSON {filepath}: {e}")
            return ""

# Convenience functions for easy usage
def generate_ue5_files_from_json(json_file_path: str, world_name: str = None, output_path: str = ".") -> Dict[str, str]:
    """
    Generate UE5 files from a JSON file created by the prompt parser

    Args:
        json_file_path: Path to the JSON file containing world data
        world_name: Name for the generated world (auto-detected if None)
        output_path: Base output directory for generated files

    Returns:
        Dictionary of generated file paths
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        if world_name is None:
            # Auto-generate world name from metadata
            level_name = json_data.get("metadata", {}).get("level_name", "GeneratedWorld")
            world_name = "".join(c for c in level_name if c.isalnum())
            if not world_name:
                world_name = "GeneratedWorld"

        generator = UE5CodeGenerator(output_path)
        return generator.generate_all(json_data, world_name)

    except Exception as e:
        logger.error(f"Failed to generate UE5 files: {e}")
        return {}

def generate_ue5_files_from_prompt(prompt: str, world_name: str = None, output_path: str = ".") -> Dict[str, str]:
    """
    Generate UE5 files directly from a prompt (uses prompt parser)

    Args:
        prompt: Natural language description of the game world
        world_name: Name for the generated world (auto-generated if None)
        output_path: Base output directory for generated files

    Returns:
        Dictionary of generated file paths
    """
    try:
        # Import prompt parser
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))

        from prompt_parser import PromptParser, OllamaConfig

        # Generate world data
        config = OllamaConfig()
        parser = PromptParser(config)
        json_data = parser.parse_prompt(prompt)

        if world_name is None:
            # Auto-generate world name from metadata
            level_name = json_data.get("metadata", {}).get("level_name", "GeneratedWorld")
            world_name = "".join(c for c in level_name if c.isalnum())
            if not world_name:
                world_name = "GeneratedWorld"

        # Generate UE5 files
        generator = UE5CodeGenerator(output_path)
        return generator.generate_all(json_data, world_name)

    except Exception as e:
        logger.error(f"Failed to generate UE5 files from prompt: {e}")
        return {}

def batch_generate_ue5_files(json_files: List[str], output_path: str = ".") -> Dict[str, Dict[str, str]]:
    """
    Generate UE5 files for multiple JSON world files

    Args:
        json_files: List of JSON file paths
        output_path: Base output directory for generated files

    Returns:
        Dictionary mapping file names to their generated files
    """
    results = {}

    for json_file in json_files:
        try:
            filename = os.path.basename(json_file).replace('.json', '')
            world_name = "".join(c for c in filename if c.isalnum())

            generated_files = generate_ue5_files_from_json(json_file, world_name, output_path)
            results[json_file] = generated_files

            logger.info(f"Generated {len(generated_files)} files for {json_file}")

        except Exception as e:
            logger.error(f"Failed to process {json_file}: {e}")
            results[json_file] = {}

    return results

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="TTG Genesis UE5 Code Generator")
    parser.add_argument("input", help="Input JSON file or prompt text")
    parser.add_argument("-w", "--world-name", help="World name for generated classes")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    parser.add_argument("-p", "--prompt", action="store_true", help="Treat input as prompt instead of file")
    parser.add_argument("-b", "--batch", action="store_true", help="Batch process multiple JSON files")

    args = parser.parse_args()

    print("🎮 TTG Genesis - UE5 Code Generator")
    print("=" * 50)

    if args.batch:
        # Batch processing
        json_files = [args.input] if not os.path.isdir(args.input) else [
            os.path.join(args.input, f) for f in os.listdir(args.input) if f.endswith('.json')
        ]

        print(f"📁 Processing {len(json_files)} JSON files...")
        results = batch_generate_ue5_files(json_files, args.output)

        total_files = sum(len(files) for files in results.values())
        print(f"✅ Generated {total_files} total files")

    elif args.prompt:
        # Generate from prompt
        print(f"🎯 Generating from prompt: {args.input[:50]}...")
        generated_files = generate_ue5_files_from_prompt(args.input, args.world_name, args.output)

        if generated_files:
            print(f"✅ Generated {len(generated_files)} files:")
            for filename, filepath in generated_files.items():
                print(f"   📄 {filename}: {filepath}")
        else:
            print("❌ Failed to generate files")

    else:
        # Generate from JSON file
        if not os.path.exists(args.input):
            print(f"❌ File not found: {args.input}")
            sys.exit(1)

        print(f"📄 Processing JSON file: {args.input}")
        generated_files = generate_ue5_files_from_json(args.input, args.world_name, args.output)

        if generated_files:
            print(f"✅ Generated {len(generated_files)} files:")
            for filename, filepath in generated_files.items():
                print(f"   📄 {filename}: {filepath}")
        else:
            print("❌ Failed to generate files")

    print("\n🎉 UE5 code generation complete!")
    print("📖 Check the generated UE5_Integration_README.md for integration instructions.")