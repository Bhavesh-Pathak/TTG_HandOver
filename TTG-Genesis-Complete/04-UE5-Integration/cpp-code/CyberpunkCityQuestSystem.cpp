#include "CyberpunkCityQuestSystem.h"
#include "Engine/Engine.h"
#include "Misc/FileHelper.h"
#include "HAL/PlatformFilemanager.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonReader.h"

ACyberpunkCityQuestSystem::ACyberpunkCityQuestSystem()
{
    PrimaryActorTick.bCanEverTick = false;

    // Initialize quest data from generated JSON
    LoadQuestsFromJSON();
}

void ACyberpunkCityQuestSystem::BeginPlay()
{
    Super::BeginPlay();

    UE_LOG(LogTemp, Warning, TEXT("CyberpunkCity Quest System initialized with %d quests"), Quests.Num());
}

bool ACyberpunkCityQuestSystem::StartQuest(const FString& QuestID)
{
    for (FCyberpunkCityQuest& Quest : Quests)
    {
        if (Quest.QuestID == QuestID && Quest.Status == EQuestStatus::NotStarted)
        {
            // Check requirements
            bool RequirementsMet = true;
            for (const FString& Requirement : Quest.Requirements)
            {
                if (!IsQuestCompleted(Requirement))
                {
                    RequirementsMet = false;
                    break;
                }
            }

            if (RequirementsMet)
            {
                Quest.Status = EQuestStatus::InProgress;
                ActiveQuests.Add(Quest);
                OnQuestStarted.Broadcast(Quest);

                UE_LOG(LogTemp, Warning, TEXT("Started quest: %s"), *Quest.QuestName);
                return true;
            }
            else
            {
                UE_LOG(LogTemp, Warning, TEXT("Quest requirements not met: %s"), *Quest.QuestName);
                return false;
            }
        }
    }

    UE_LOG(LogTemp, Warning, TEXT("Quest not found or already started: %s"), *QuestID);
    return false;
}

bool ACyberpunkCityQuestSystem::CompleteQuest(const FString& QuestID)
{
    for (int32 i = 0; i < ActiveQuests.Num(); i++)
    {
        if (ActiveQuests[i].QuestID == QuestID)
        {
            FCyberpunkCityQuest CompletedQuest = ActiveQuests[i];
            CompletedQuest.Status = EQuestStatus::Completed;

            // Update main quest array
            for (FCyberpunkCityQuest& Quest : Quests)
            {
                if (Quest.QuestID == QuestID)
                {
                    Quest.Status = EQuestStatus::Completed;
                    break;
                }
            }

            CompletedQuests.Add(CompletedQuest);
            ActiveQuests.RemoveAt(i);
            OnQuestCompleted.Broadcast(CompletedQuest);

            UE_LOG(LogTemp, Warning, TEXT("Completed quest: %s"), *CompletedQuest.QuestName);
            return true;
        }
    }

    UE_LOG(LogTemp, Warning, TEXT("Active quest not found: %s"), *QuestID);
    return false;
}

bool ACyberpunkCityQuestSystem::IsQuestActive(const FString& QuestID) const
{
    for (const FCyberpunkCityQuest& Quest : ActiveQuests)
    {
        if (Quest.QuestID == QuestID)
        {
            return true;
        }
    }
    return false;
}

bool ACyberpunkCityQuestSystem::IsQuestCompleted(const FString& QuestID) const
{
    for (const FCyberpunkCityQuest& Quest : CompletedQuests)
    {
        if (Quest.QuestID == QuestID)
        {
            return true;
        }
    }
    return false;
}

FCyberpunkCityQuest ACyberpunkCityQuestSystem::GetQuest(const FString& QuestID) const
{
    for (const FCyberpunkCityQuest& Quest : Quests)
    {
        if (Quest.QuestID == QuestID)
        {
            return Quest;
        }
    }
    return FCyberpunkCityQuest();
}

TArray<FCyberpunkCityQuest> ACyberpunkCityQuestSystem::GetActiveQuests() const
{
    return ActiveQuests;
}

TArray<FCyberpunkCityQuest> ACyberpunkCityQuestSystem::GetAvailableQuests() const
{
    TArray<FCyberpunkCityQuest> AvailableQuests;

    for (const FCyberpunkCityQuest& Quest : Quests)
    {
        if (Quest.Status == EQuestStatus::NotStarted)
        {
            // Check if requirements are met
            bool RequirementsMet = true;
            for (const FString& Requirement : Quest.Requirements)
            {
                if (!IsQuestCompleted(Requirement))
                {
                    RequirementsMet = false;
                    break;
                }
            }

            if (RequirementsMet)
            {
                AvailableQuests.Add(Quest);
            }
        }
    }

    return AvailableQuests;
}

void ACyberpunkCityQuestSystem::LoadQuestsFromJSON()
{
    // Load quest data from generated JSON file
    FString FilePath = FPaths::ProjectContentDir() + TEXT("Data/QuestData.json");
    FString JsonString;

    if (FFileHelper::LoadFileToString(JsonString, *FilePath))
    {
        TSharedPtr<FJsonObject> JsonObject;
        TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

        if (FJsonSerializer::Deserialize(Reader, JsonObject))
        {
            const TArray<TSharedPtr<FJsonValue>>* QuestArray;
            if (JsonObject->TryGetArrayField(TEXT("quests"), QuestArray))
            {
                for (const TSharedPtr<FJsonValue>& QuestValue : *QuestArray)
                {
                    const TSharedPtr<FJsonObject>& QuestObj = QuestValue->AsObject();

                    FCyberpunkCityQuest NewQuest;
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
                    {
                        for (const TSharedPtr<FJsonValue>& ReqValue : *RequirementsArray)
                        {
                            NewQuest.Requirements.Add(ReqValue->AsString());
                        }
                    }

                    // Parse rewards
                    const TSharedPtr<FJsonObject>* RewardsObj;
                    if (QuestObj->TryGetObjectField(TEXT("rewards"), RewardsObj))
                    {
                        NewQuest.Rewards.Experience = (*RewardsObj)->GetIntegerField(TEXT("experience"));
                        NewQuest.Rewards.Gold = (*RewardsObj)->GetIntegerField(TEXT("gold"));

                        const TArray<TSharedPtr<FJsonValue>>* ItemsArray;
                        if ((*RewardsObj)->TryGetArrayField(TEXT("items"), ItemsArray))
                        {
                            for (const TSharedPtr<FJsonValue>& ItemValue : *ItemsArray)
                            {
                                NewQuest.Rewards.Items.Add(ItemValue->AsString());
                            }
                        }
                    }

                    Quests.Add(NewQuest);
                }
            }
        }
    }
    else
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load quest data from: %s"), *FilePath);
    }
}